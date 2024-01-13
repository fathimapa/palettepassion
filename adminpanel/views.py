from ctypes import cast
import functools,random
import datetime
from django.forms import DateTimeField, FloatField
from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib import messages , auth
from django.views import View
from accounts.models import Account
from banner_management.models import Banner
from category.models import category
from store.models import * 
from .forms import *
from accounts.forms import RegisterationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache,cache_control
from django.http import HttpResponse ,JsonResponse
from django.utils import timezone
from django.utils.text import slugify
from category.form import CategoryForm
from store.form import AddProductForm
from django.views.generic import ListView
from django.db import transaction
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.db.models import Q,Sum,Count
from django.urls import reverse_lazy
from order.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime,timedelta,date
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay,TruncYear
from django.db.models.functions import ExtractYear,ExtractMonth,ExtractWeek
from calendar import month_name
import calendar
from django.core.paginator import Paginator
from django.db.models import Sum, Case, When, Value, IntegerField
from django.db.models import Count, Q, F, ExpressionWrapper, DurationField










# Create your views here.


#---------------------------------------------------------------#
#------------------Admin Dashboard Managemenet------------------#
#---------------------------------------------------------------#

def check_isadmin(view_func, redirect_url="admin_signin" , message="You need to be logged in as an admin to access this page"):
    """
        used to check loged one was admin or not
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superadmin:
            return view_func(request,*args, **kwargs)
        messages.error(request,message)
        redirect_url_ = reverse(redirect_url)+'?next='+request.path
        return redirect(redirect_url_)
    return wrapper

class AdminRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return check_isadmin(view)


#------------------Admin Sign In-----------------#



def admin_signin(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            if user.is_superadmin:
                auth.login(request,user)
                return redirect('admin_dashboard') 
            else:
                messages.error(request, "Not a superuser")
                return redirect('admin_signin') 
            
        else:
            messages.error(request, "Invalid username")
            return redirect('admin_signin') 

        
    return render(request,'adminpanel/admin_signin.html')



#------------------Admin Dashboard-----------------#




@check_isadmin
def admin_dashboard(request):
    users_count = Account.objects.filter(is_active = True).count()
    sales = Order.objects.filter(is_ordered=True).exclude(status__in=["Cancelled", "Returned"]).aggregate(total_sales=Sum('order_total'))
    total_sales = 0
    if sales['total_sales'] is not None:
        total_sales = float(sales['total_sales'])

    active_products_count = Variation.objects.filter(is_active=True,product__is_active=True).count()
    coupon_count = Coupon.objects.filter(active = True).count()
    categories_count = category.objects.filter(is_active=True).count()
    banner_count = Banner.objects.filter(is_active = True).count()


    recent_signups = Account.objects.all().order_by('-date_joined')[:10]
    recent_payments = Payment.objects.all().order_by('-order_id')[:10]


    today = datetime.today()
    today_date = today.strftime("%Y-%m-%d")
    

    # over all payment count 
    paypal_orders = Payment.objects.filter(payment_method="Paypal",status = 'True').count()
    cash_on_delivery_count = Payment.objects.filter(payment_method="Cash on Delivery",status = 'True').count()
    wallet_payment = Payment.objects.filter(payment_method="Wallet payment",status = 'True').count()

    # over all user count 
    blocked_user = Account.objects.filter(is_active = False,is_superadmin = False).count()
    unblocked_user = Account.objects.filter(is_active = True,is_superadmin = False).count()

    # over all Sales count 
    today_sale = Order.objects.filter(created_at = today_date,payment__status = 'True', is_ordered=True).count()
    print(today_sale)
    today = today.strftime("%A")
    new_date = datetime.today() - timedelta(days = 1)
    yester_day_sale =   Order.objects.filter(created_at = new_date,payment__status = 'True', is_ordered=True).count()  
    yesterday = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_2 = Order.objects.filter(created_at = new_date,payment__status = 'True', is_ordered=True).count()
    day_2_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_3 = Order.objects.filter(created_at = new_date,payment__status = 'True', is_ordered=True).count()
    day_3_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_4 = Order.objects.filter(created_at = new_date,payment__status = 'True', is_ordered=True).count()
    day_4_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_5 = Order.objects.filter(created_at = new_date,payment__status = 'True', is_ordered=True).count()
    day_5_name = new_date.strftime("%A")



    # Yearly Sales data

    current_year = date.today().year
    years = list(range(current_year, current_year - 5, -1))
    yearly_sales = (
        Order.objects.filter(payment__status='True', is_ordered=True)
        .annotate(year=ExtractYear('created_at'))
        .values('year')
        .annotate(count=Count('id'))
    )
    sales_dict = {entry['year']: entry['count'] for entry in yearly_sales}
    yearly_sales_list = [{'year': year, 'count': sales_dict.get(year, 0)} for year in years]
    print("loo" ,yearly_sales_list)
    



    # Monthly Sales data

    month_queries = [Q(created_at__month=month, created_at__year=current_year) for month in range(1, 13)]
    combined_query = Q()
    for query in month_queries:
        combined_query |= query
    # Filter the orders using the combined_query
    output = (
        Order.objects.filter(combined_query, is_ordered=True)
        .annotate(month=ExtractMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
    )
    output_dict = {entry['month']: entry['count'] for entry in output}
    monthly_sales_list = [
        {'month_name': calendar.month_name[month], 'count': output_dict.get(month, 0)}
        for month in range(1, 13)
    ]
    print(monthly_sales_list)




    # Weekly Sales data
    
    current_year = timezone.now().year
    start_of_year = timezone.datetime(current_year, 1, 1)
    end_of_year = timezone.datetime(current_year + 1, 1, 1)
    
    # Filter orders within the current year and those with successful payments
    orders = Order.objects.filter(
        created_at__gte=start_of_year, created_at__lt=end_of_year, payment__status='True', is_ordered=True
    )
    
    # Annotate with week and year
    weekly_sales = (
        orders.annotate(
            week=ExpressionWrapper(F('created_at') - DurationField('7 days'), output_field=DateTimeField()),
            week_number=ExtractWeek('created_at'),
            year=ExtractYear('created_at'),
        )
        .values('week_number', 'year')
        .annotate(count=Count('id'))
        .order_by('week_number')
    )
    
    # Construct a list with week numbers and counts
    weekly_sales_list = [
        {'week': f"Week {entry['week_number']}", 'count': entry['count']} for entry in weekly_sales
    ]
    
    
    daily_sales = (
        Order.objects.filter(payment__status='True', is_ordered=True)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
        .values_list('day', 'count')
    )
    
    daily_sales_list = [{'day': day, 'count': count} for day, count in daily_sales]



    #over all order status count
    ordered = Order.objects.filter(is_ordered=True,status = 'Order Confirmed').count()
    shipped = Order.objects.filter(is_ordered=True,status = "Shipped").count()
    out_of_delivery = Order.objects.filter(is_ordered=True,status ="Out for delivery").count()
    delivered = Order.objects.filter(is_ordered=True,status = "Delivered").count()
    returned = Order.objects.filter(is_ordered=True,status = "Returned").count()
    cancelled = Order.objects.filter(is_ordered=True,status = "Cancelled").count()

    context ={
        'yearly_sales_list': yearly_sales_list,
        'monthly_sales_list': monthly_sales_list,
        'weekly_sales': weekly_sales_list,
        'daily_sales': daily_sales_list,
        'paypal_orders':paypal_orders,
        'wallet_payment':wallet_payment,
        'ordered':ordered,
        'shipped':shipped,
        'out_of_delivery':out_of_delivery,
        'delivered':delivered,
        'returned':returned,
        'cancelled':cancelled,
        'cash_on_delivery_count':cash_on_delivery_count,
        'blocked_user':blocked_user,
        'unblocked_user':unblocked_user,
        'today_sale':today_sale,
        'yester_day_sale':yester_day_sale,
        'day_2':day_2,
        'day_3':day_3,
        'day_4':day_4,
        'day_5':day_5,
        'today':today,
        'yesterday':yesterday,
        'day_2_name':day_2_name,
        'day_3_name':day_3_name,
        'day_4_name':day_4_name,
        'day_5_name':day_5_name,
        "users_count":users_count,
        "total_sales":total_sales,
        "active_products_count":active_products_count,
        'coupon_count':coupon_count,
        'categories_count':categories_count,
        'recent_signups':recent_signups,
        'recent_payments':recent_payments,
        'banner_count':banner_count,
    }


    return render(request,'adminpanel/index.html',context)



class DashboardSalesData(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, format=None):
        total_orders_count  = Order.objects.filter(is_ordered=True).count()
        new_orders_count  = Order.objects.filter(is_ordered=True,status='Order_Confirmed').count()
        shipped_orders_count  = Order.objects.filter(is_ordered=True,status='Shipped').count()
        out_for_Delivery_orders_count  = Order.objects.filter(is_ordered=True,status='Out_for_delivery').count()
        cancelled_orders_count  = Order.objects.filter(is_ordered=True,status="Cancelled").count()
        returned_orders_count  = Order.objects.filter(is_ordered=True,status='Returned').count()
        delivered_orders_count  = Order.objects.filter(is_ordered=True,status='Delivered').count()
        data = {
            'status':'success',
            'data':{
                'Total Orders':total_orders_count,
                'New Orders':new_orders_count,
                'shipped_orders_count':shipped_orders_count,
                'out_for_Delivery_orders_count':out_for_Delivery_orders_count,
                'cancelled Orders':cancelled_orders_count,
                'Returned Orders':returned_orders_count,
                'Delivered Orders':delivered_orders_count,
                }    
        }
        return Response(data)





#------------------Admin Logout-----------------#



@login_required(login_url='admin_signin')
def admin_logout(request):
    auth.logout(request)
    return redirect('admin_signin')



#----------------------------------------------------------#
#------------------Admin User Managemenet------------------#
#----------------------------------------------------------#


@check_isadmin
def admin_user_management(request):
    users = Account.objects.all()
    context={
        
        'users' : users,
    }
    return render(request, 'adminpanel/admin_user_management.html',context)




#------------------Admin Side Create User as Staff-----------------#


@check_isadmin
def create_user_from_admin(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            # Create a new user
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.is_active = True
            user.is_staff = True
            user.save()

            messages.success(request, 'User creation successful')
            return redirect('admin_user_management')

    else:
        form = RegisterationForm()

    context = {
        'form': form,
    }

    return render(request, 'adminpanel/create_user.html', context)



#------------------Admin Side User Block Unblock-----------------#


@check_isadmin
def admn_users_block_unblock(request):
    combined_message = ""
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_id[]')
        status = request.POST.get("action_type")
        new_var = True if status == "ACTIVE" else False

        for user_id in user_ids:
            try:
                user = Account.objects.get(id=user_id)
                user.is_active = new_var
                user.save()
                
                combined_message += f"User {user.username} updated to {status}\n"
            except Account.DoesNotExist:
                combined_message += f"User with ID {user_id} does not exist\n"
            except Exception as e:
                combined_message += f"Error updating user: {str(e)}\n"
 
    if combined_message:
        messages.success(request, combined_message) 
        
    users = Account.objects.all()
    return render(request, 'adminpanel/admin_user_management.html', {'users': users})



#--------------------------------------------------------------#
#------------------Admin Category Managemenet------------------#
#--------------------------------------------------------------#



@check_isadmin
def admin_category_management(request):
    categories = category.objects.all()
    context={
        
        'categories' : categories,
    }
    return render(request, 'adminpanel/admin_category_management.html',context)




#------------------Admin Side Edit Category-----------------#


class CategoryUpdateView(AdminRequiredMixin,UpdateView):
    model = category
    form_class = CategoryForm
    template_name = "adminpanel/edit_category.html"

    def get_success_url(self):
        return reverse_lazy("admin_category_management")
    


#------------------Admin Side Add Category-----------------#

@check_isadmin
def add_category(request): 
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()  # This will automatically fill the slug based on clean() method
            return redirect('admin_category_management')
    else:
        form = CategoryForm()
    
    return render(request, 'adminpanel/add_category.html', {'form': form})

#------------------Admin Side Block Ublock Category-----------------#


@check_isadmin
def admn_category_block_unblock(request):
    combined_message = ""
    
    if request.method == 'POST':
        category_ids = request.POST.getlist('category_id[]')
        status = request.POST.get("action_type")
        new_var = True if status == "ACTIVE" else False

        with transaction.atomic():  # Use a transaction to ensure consistency
            for category_id in category_ids:
                try:
                    category_obj = category.objects.get(id=category_id)
                    category_obj.is_active = new_var
                    category_obj.save()

                    # Update the status of products under the category
                    category_obj.products.update(is_active=new_var)

                    combined_message += f"Category {category_obj.category_name} updated to {status}\n"
                except category.DoesNotExist:
                    combined_message += f"Category with ID {category_id} does not exist\n"
                except Exception as e:
                    combined_message += f"Error updating Category: {str(e)}\n"

    if combined_message:
        messages.success(request, combined_message)

    categories = category.objects.all()
    return render(request, 'adminpanel/admin_category_management.html', {'categories': categories})



#-------------------------------------------------------------#
#------------------Admin Product Managemenet------------------#
#-------------------------------------------------------------#



@check_isadmin
def admn_product_block_unblock(request):
    combined_message = ""
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_id[]')
        status = request.POST.get("action_type")
        new_var = True if status == "ACTIVE" else False

        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
                if product.category.is_active == False:
                    combined_message += f"Error updating Product: {product.product_name} because category is Inactive"
                else:                    
                    product.is_active = new_var
                    product.save()
                    combined_message += f"Product {product.product_name} updated to {status}\n"
            except Account.DoesNotExist:
                combined_message += f"Product with ID {product_id} does not exist\n"
            except Exception as e:
                combined_message += f"Error updating Product: {str(e)}\n"
 
    if combined_message:
        messages.success(request, combined_message) 
        
    products = Product.objects.all()
    return render(request, 'adminpanel/product_list.html', {'products': products})




#-------------------------------------------------------------#
#------------------Admin Variation Managemenet----------------#
#-------------------------------------------------------------#


class VariationList(AdminRequiredMixin,ListView):
    model = Variation
    template_name = "adminpanel/variation_list.html"
    context_object_name = "variations"


#------------------Admin Side Add Variation-----------------#


class VariationCreateVeiw(AdminRequiredMixin,CreateView):
    model = Variation
    form_class = VariationForm
    template_name = "adminpanel/variation_create_or_update.html"

    def form_valid(self, form):
        product_id = form.cleaned_data['product'] 
        product = Product.objects.get(pk=product_id.pk)
        form.instance.product = product
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("variationlist")



#------------------Admin Side Edit Variation-----------------#


class VariationUpdateView(AdminRequiredMixin,UpdateView):
    model = Variation
    form_class = VariationForm
    template_name = "adminpanel/variation_create_or_update.html"

    def get_success_url(self):
        return reverse_lazy("variationlist")

#------------------Admin Side Block and Ublock Variation-----------------#

class VariationBlockOrUnblockView(AdminRequiredMixin,View):
    template_name = 'adminpanel/variation_list.html'

    def post(self,request,*args,**kwargs):

        combined_message = ""
        variation_ids = request.POST.getlist('variation_id[]')
        status = request.POST.get("action_type")
        new_status = True if status == "ACTIVE" else False

        for variation_id in variation_ids:
            try:
                variation = get_object_or_404(Variation, id = variation_id)
                if variation.is_active is False:
                    combined_message += f"Error updating Variation: {variation.size} because category is Inactive\n"

                else:
                    variation.is_active = new_status
                    variation.save()
                    combined_message = f"Variation {variation.size} of Product {variation.product.product_name} updated to {status}\n"

            except Variation.DoesNotExist:
                combined_message = f"Variation with ID {variation_id} does not exist\n"

            except Exception as e:
                combined_message += f"Error updating Variation: {str(e)}\n"

        if combined_message:
            messages.success(request, combined_message)

        variations = Variation.objects.all()
        return render(request , self.template_name, {'variations':variations})
        

#--------------------------------------------------------------#
#---------------------Admin Order Management-------------------#
#--------------------------------------------------------------#


class OrderList(AdminRequiredMixin,ListView):
    model = Order
    template_name = "adminpanel/order_list.html"
    context_object_name = "orders"


#------------------Admin Side Edit Order-----------------#

class OrderUpdateView(AdminRequiredMixin,UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "adminpanel/order_update.html"

    def get_success_url(self):
        return reverse_lazy("orderlist")


#--------------------------------------------------------------#
#---------------------Admin Coupon Management------------------#
#--------------------------------------------------------------#

class CouponList(AdminRequiredMixin,ListView):
    model = Coupon
    template_name = "adminpanel/coupon_list.html"
    context_object_name = "coupons"


#------------------Admin Side Add Coupon-----------------#

class CouponCreateView(AdminRequiredMixin,CreateView):
    model = Coupon
    form_class = CouponForm
    template_name = "adminpanel/coupon_create_or_update.html"  

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("CouponList") 



#------------------Admin Side Edit Coupon-----------------#


class CouponUpdateView(AdminRequiredMixin,UpdateView):
    model = Coupon
    form_class = CouponForm
    template_name = "adminpanel/coupon_create_or_update.html"

    def get_success_url(self):
        return reverse_lazy("CouponList")
    

#------------------Admin Side block and unblock Coupon-----------------#

class CouponBlockOrUnblockView(AdminRequiredMixin,View):
    template_name = 'adminpanel/coupon_list.html'  # Adjust template path as needed

    def post(self, request, *args, **kwargs):
        combined_message = ""
        coupon_ids = request.POST.getlist('coupon_id[]')
        status = request.POST.get("action_type")
        new_status = True if status == "ACTIVE" else False

        for coupon_id in coupon_ids:
            try:
                coupon = get_object_or_404(Coupon, id=coupon_id)
                coupon.active = new_status
                coupon.save()
                combined_message += f"Coupon {coupon.code} updated to {status}\n"

            except Coupon.DoesNotExist:
                combined_message += f"Coupon with ID {coupon_id} does not exist\n"

            except Exception as e:
                combined_message += f"Error updating Coupon: {str(e)}\n"

        if combined_message:
            messages.success(request, combined_message)

        coupons = Coupon.objects.all()
        return render(request, self.template_name, {'coupons': coupons})

#--------------------------------------------------------------#
#---------------------Admin Banner Management------------------#
#--------------------------------------------------------------#

class BannerList(AdminRequiredMixin,ListView):
    model = Banner
    template_name = "adminpanel/banner_list.html"
    context_object_name = "banners"


#------------------Admin Side Add Banner-----------------#

class BannerCreateView(CreateView):
    model = Banner
    form_class = BannerForm
    template_name = "adminpanel/banner_create_or_update.html"  

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("BannerList") 
    

#------------------Admin Side Edit Banner-----------------#

class BannerUpdateView(AdminRequiredMixin,UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = "adminpanel/banner_create_or_update.html"

    def get_success_url(self):
        return reverse_lazy("BannerList")
    
#------------------Admin Side Block and Unblock Banner-----------------#


class BannerBlockOrUnblockView(AdminRequiredMixin,View):
    template_name = 'adminpanel/banner_list.html'  # Adjust template path as needed

    def post(self, request, *args, **kwargs):
        combined_message = ""
        banner_ids = request.POST.getlist('banner_id[]')
        status = request.POST.get("action_type")
        new_status = True if status == "ACTIVE" else False

        for banner_id in banner_ids:
            try:
                banner = get_object_or_404(Banner, id=banner_id)
                banner.is_active = new_status
                banner.save()
                combined_message += f"Banner {banner.banner_name} updated to {status}\n"

            except Banner.DoesNotExist:
                combined_message += f"Banner with ID {banner_id} does not exist\n"

            except Exception as e:
                combined_message += f"Error updating Banner: {str(e)}\n"

        if combined_message:
            messages.success(request, combined_message)

        banners = Banner.objects.all()
        return render(request, self.template_name, {'banners': banners})
    
#----------------------------------------------------------#
#------------------Admin Sales Report ---------------------#
#----------------------------------------------------------#
    
@check_isadmin
def salesReport(request):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    years = []
    today_date=str(date.today())
    start_date=today_date
    end_date=today_date


    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        val = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = val+timedelta(days=1)

        orders = Order.objects.filter(
            Q(created_at__lte=end_date),
            Q(created_at__gte=start_date),
            payment__status='True'
        ).values(
            'user_order_page__product__product_name',
            'user_order_page__product__variation__stock',
            'user_order_page__product__variation__size',
        ).annotate(
            total=Sum(
                Case(
                    When(user_order_page__product__variation__size='small', then='order_total'),
                    When(user_order_page__product__variation__size='medium', then='order_total'),
                    When(user_order_page__product__variation__size='large', then='order_total'),
                    When(user_order_page__product__variation__size='extralarge', then='order_total'),

                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            dcount=Sum('user_order_page__quantity')
        ).order_by('-total')

        # orders = Order.objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__variation__stock','user_order_page__product__variation__size',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
        
        print("hello",orders.values('user_order_page__product__variation__size'))

    else:
        orders = Order.objects.filter(
            Q(created_at__lte=end_date),
            Q(created_at__gte=start_date),
            payment__status='True'
        ).values(
            'user_order_page__product__product_name',
            'user_order_page__product__variation__stock',
            'user_order_page__product__variation__size',
        ).annotate(
            total=Sum(
                Case(
                    When(user_order_page__product__variation__size='small', then='order_total'),
                    When(user_order_page__product__variation__size='medium', then='order_total'),
                    When(user_order_page__product__variation__size='large', then='order_total'),
                    When(user_order_page__product__variation__size='extralarge', then='order_total'),

                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            dcount=Sum('user_order_page__quantity')
        ).order_by('-total')
        # orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__variation_stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total') 
        print("hello",orders.values('user_order_page__product__variation'))
        
    year = today.year
    for i in range (4):
        val = year-i
        years.append(val)

    


    context = {
        'orders':orders,
        'today_date':today_date,
        'years':years,
        'start_date':start_date,
        'end_date':end_date,
    
    }
    
    
    return render(request,'adminpanel/salesReport.html',context)


@check_isadmin
def salesReportMonth(request,id):
    orders = Order.objects.filter(created_at__month = id,payment__status = 'True').values('user_order_page__product__product_name',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    paginator = Paginator(orders,7)
    page= request.GET.get('page')
    paged_report = paginator.get_page(page) 
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }
    return render(request,'adminpanel/salesReportTable.html',context)


@check_isadmin
def salesReportYear(request,id):
    orders = Order.objects.filter(created_at__year = id,payment__status = 'True').values('user_order_page__product__product_name',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    paginator = Paginator(orders,7)
    page= request.GET.get('page')
    paged_report = paginator.get_page(page)    
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }
    return render(request,'adminpanel/salesReportTable.html',context) 
