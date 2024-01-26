from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import render,redirect
from store.models import Product
from accounts.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages , auth
from order.models import *
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from .forms import *
from banner_management.models import *
# from core.renderer
import jinja2
import pdfkit
import random
import string
import tempfile
import os
from .models import *
from django.core.exceptions import PermissionDenied

# Create your views here.

def index(request):
    products = Product.objects.all().filter(is_active = True)
    banners = Banner.objects.filter(is_active=True)

    context = {
        'products' : products,
        'banners':banners,
    }
    return render(request , 'userside/core/index.html',context)

def dashboard(request):
    userprofile = UserProfile.objects.get(user=request.user)
    context= {
        'userprofile':userprofile,
        }

    return render(request , 'userside/userprofile/dashboard.html',context)


@login_required(login_url='login')
def edit_profile(request):
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        userprofile = UserProfile(user = request.user)
        userprofile.save()
    if request.method == 'POST':
        user_form = EditForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
        else:
            for field_name , error_messages in user_form.errors.items():
                print("error in" ,field_name,error_messages)
            return redirect('edit_profile')
    else:
        user_form = EditForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context= {
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
        }
    return render(request,'userside/userprofile/edit_profile.html',context)


@login_required(login_url='login')
def change_password(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = Account.objects.get(email__exact=request.user.email)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                #auth.logout(request)
                messages.success(request,'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request,'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request,'Password does not match!')
            return redirect('change_password')
        
    context = {
        "userprofile":userprofile,
    }

    return render(request,'userside/userprofile/change_password.html',context)



@login_required(login_url='login')
def my_address(request):
    current_user = request.user
    userprofile = UserProfile.objects.get(user=current_user)
    address = Address.objects.filter(user=current_user)
    items_per_page = 10
    paginator = Paginator(address,items_per_page)
    page= request.GET.get('page')
    paged_address = paginator.get_page(page)

    context = {
        'address':paged_address,
        "userprofile":userprofile,
    }
    return render(request,'userside/userprofile/my_address.html',context)

@login_required(login_url='login')
def addAddress(request):
    if request.method == 'POST':
        # print(request.user)
        # userprofile = UserProfile.objects.get(user=request.user)
        form = AddressForm(request.POST,request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line1 =  form.cleaned_data['address_line1']
            detail.address_line2  = form.cleaned_data['address_line2']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.country = form.cleaned_data['country']
            detail.zipcode = form.cleaned_data['zipcode']
            detail.save()
            messages.success(request,'Address added Successfully')
            return redirect('my_address')
        else:
            messages.success(request,'Form is Not valid')
            return redirect('my_address')
    else:
        form = AddressForm()
        context={
            'form':form,
            # 'userprofile':userprofile,
        }    
    return render(request,'userside/userprofile/add_address.html',context)


@login_required(login_url='login')
def editAddress(request, id):
    userprofile = UserProfile.objects.get(user=request.user)
    address = Address.objects.get(id=id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request , 'Address Updated Successfully')
            return redirect('my_address')
        else:
            messages.error(request , 'Invalid Inputs!!!')
            return redirect('my_address')
    else:
        form = AddressForm(instance=address)

    context = {
            'form' : form,
            'userprofile':userprofile
        }
    return render(request,'userside/userprofile/edit_address.html',context)



@login_required(login_url='login')
def deleteAddress(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('my_address')


#checkout
def deleteCheckoutAddress(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('checkout')



def AddCheckoutAddress(request):
    if request.method == 'POST':
        # print(request.user)
        # userprofile = UserProfile.objects.get(user=request.user)
        form = AddressForm(request.POST,request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line1 =  form.cleaned_data['address_line1']
            detail.address_line2  = form.cleaned_data['address_line2']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.country = form.cleaned_data['country']
            detail.zipcode = form.cleaned_data['zipcode']
            detail.save()
            messages.success(request,'Address added Successfully')
            return redirect('checkout')
        else:
            messages.success(request,'Form is Not valid')
            return redirect('checkout')
    else:
        form = AddressForm()

@login_required(login_url='login')
def my_orders(request):
    userprofile = UserProfile.objects.get(user=request.user)
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-id')

    paginator = Paginator(orders,8)
    page= request.GET.get('page')
    paged_users = paginator.get_page(page)
    today = date.today()
    

    context = {
        'orders': paged_users, 
        'today':today,
        'userprofile':userprofile,
    }

    return render(request,'userside/userprofile/my_orders.html',context)

def my_wallet(request):
    userprofile = UserProfile.objects.get(user=request.user)
    context= {
        'userprofile':userprofile,
    }
    return render(request,'userside/userprofile/my_wallet.html',context)

def my_wishlist(request):
    userprofile = UserProfile.objects.get(user=request.user)
    context = {
        "userprofile": userprofile,
    }
    return render(request,'userside/userprofile/my_wishlist.html',context)

def error(request, exception = None):
    return render(request, 'userside/error/error.html', status=404)

# def permission_denied_view(request):
#     raise PermissionDenied

@login_required(login_url='login')
def order_details(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    userprofile = UserProfile.objects.get(user = request.user)
    orders = Order.objects.get(order_number=order_id)
    total=0
    for i in order_detail:
            i.product.price = i.product.get_product_price_by_size_id(i.variations.pk)
            total = (i.product.price * i.quantity)
    tax = (2*total)/100
    shipping = (2*total)/100
    print('check')
    
    
    context = {
        'order_detail':order_detail,
        'orders':orders,
        'total':total,
        'tax':tax,
        'shipping':shipping,
        'userprofile':userprofile,   
    }
    return render(request,'userside/userprofile/order_details.html',context)


def generate_invoice_number(prefix, length=6):
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}-{random_part}"

def generate_invoice_pdf(request,order_id):
    user = request.user
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    userprofile = UserProfile.objects.get(user = request.user)
    orders = Order.objects.get(order_number=order_id)
    total=0
    for i in order_detail:
            i.product.price = i.product.get_product_price_by_size_id(i.variations.pk)
            total = (i.product.price * i.quantity)
    tax = (2*total)/100
    shipping = (2*total)/100

    today_date = datetime.today().strftime("%d %b, %Y")
    month = datetime.today().strftime("%B")
    invoice_number = generate_invoice_number("INV")



    context = {
        'user':user,
        'order_detail':order_detail,
        'orders':orders,
        'total':total,
        'tax':tax,
        'shipping':shipping,
        'userprofile':userprofile,  
        'today_date':today_date,
        'month':month, 
        'invoice_number':invoice_number,
    }

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    html_template = 'templates/userside/userprofile/invoice.html'  # Adjust the path based on your project structure
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    # config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')  # Adjust the path
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    # pdfkit.from_string(output_text, response, configuration=config, css='static/css/invoice.css')  # Adjust the path

    # return response
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w") as temp_html:
        temp_html.write(output_text)
        temp_html_path = temp_html.name

    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')  # Adjust the path
    pdfkit.from_url('https://www.palettepassion.shop', 'out-test.pdf', configuration=config)


    # Use the temporary HTML file path
    pdfkit.from_file(temp_html_path, 'invoice.pdf', configuration=config)  # Adjust the path

    # Remove the temporary HTML file
    os.remove(temp_html_path)

    with open('invoice.pdf', 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response
    # return render(request,'userside/userprofile/invoice.html',context)


def contact(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['user']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['sendermessage']
            Contact.objects.create(name = name ,email= email,subject =subject,message =message)
            messages.success(request, 'Message send successful')
            return redirect('contact')
    else:
        return redirect('login')

    return render(request , 'userside/core/contact.html')
