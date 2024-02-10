from datetime import datetime,date
import json
from django.shortcuts import render, redirect
from carts.models import *
from .models import *
from store.models import *
from decimal import Decimal
import hmac
from django.http import JsonResponse, HttpResponse
from django.contrib import messages , auth


# Create your views here.
def payments(request):
    user = request.user
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        order_id = order.order_number,
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = 'True',                  #body['status']
        )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    # move the cart item in to oredr product table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        item.product.price = item.product.get_product_price_by_size_id(item.size_variant.pk)
        print('size', item.size_variant.pk)     
        print(item.id)
        
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = item.product_id
        order_product.variations = item.size_variant
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save() 
        cart_item = CartItem.objects.get(id=item.id)
        if cart_item.size_variant:
            product_variation = cart_item.size_variant
        print('size', cart_item.size_variant.pk)      
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variations = product_variation
        order_product.save()
        
        # reduce the Quantity of variation
        test = cart_item.size_variant
        print(test)
        variation = Variation.objects.get(id=cart_item.size_variant.pk)
        variation.stock -= cart_item.quantity
        variation.save()
    # clear cart

    CartItem.objects.filter(user=request.user).delete()
    data = {
        'order_number':order.order_number,
        'transID':payment.payment_id
        }
    print('boss')
    return JsonResponse(data)



def payments_completed(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    print(transID, "testing transid")
    try:
        order = Order.objects.get(order_number=order_number)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        total = 0
        for i in ordered_products:
            total = (i.product.price * i.quantity)
        tax = (2*total)/100
        shipping = (2*total)/100
        
        grand_total = Decimal(str(order.order_total)) + Decimal(str(shipping))
        payment = Payment.objects.get(payment_id=transID)
        context={
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'total':total,
            'tax':tax,
            'shipping':shipping,
            
            }
        return render(request,'userside/order/payment_success.html',context)
    except Exception as e:
        print(e)
        return redirect(reverse('payment_failed'))

def place_order(request, total=0, quantity=0):
    current_user = request.user

    # if the cart count is less than or equal to 0, then redirect back to the shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        cart_item.product.price = cart_item.product.get_product_price_by_size_id(
            cart_item.size_variant.pk)
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    coupon_discount=0
    # Calculate the grand total
    shipping = (2*total)/100
    # print('check')
    # grand_total = Decimal(str(order.order_total)) + shipping
    grand_total = total + tax + shipping
    grand_total = format(grand_total, '.2f')

    if request.method == 'POST':
        print("hello")
        coupon_code = request.POST['coupon']
        # Fetch the address based on the selected address id
        address_id = request.POST.get('flexRadioDefault')
        address = Address.objects.get(user=request.user, id=address_id)
        # Create a new order
        order = Order.objects.create(
            user=current_user,
            first_name=address.first_name,
            last_name=address.last_name,
            phone=address.phone,
            email=address.email,
            address_line_1=address.address_line1,
            address_line_2=address.address_line2,
            state=address.state,
            city=address.city,
            country=address.country,
            order_note=address.order_note,
            order_total=grand_total,
            tax=tax,
            ip=request.META.get('REMOTE_ADDR')
        )
        # Generate order number
        yr = int(datetime.now().strftime('%Y'))
        dt = int(datetime.now().strftime('%d'))
        mt = int(datetime.now().strftime('%m'))
        d = date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(order.id)
        order.order_number = order_number
        order.save()
        try:
            instance = UserCoupon.objects.get(user = request.user ,coupon__code = coupon_code)
        
            if float(grand_total) >= float(instance.coupon.min_value):
                coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
                grand_total = float(grand_total) - coupon_discount
                grand_total = format(grand_total, '.2f')
                coupon_discount = format(coupon_discount, '.2f')
            order.order_total = grand_total
            order.order_discount = coupon_discount
            order.save()
        
        except:
            pass
        # Fetch the user profile
        profile = UserProfile.objects.get(user=request.user)
        context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'coupon_discount':coupon_discount,
            'grand_total': grand_total,
            'order_number': order_number,
            'profile': profile,
            'shipping':shipping,
        }

        return render(request, 'userside/order/payments.html', context)
    else:
        print('Form not valid')
        return redirect('checkout')



def cash_on_delivery(request, id):
    # Move cart item to ordered product table
    try:         
        order = Order.objects.get(
            user=request.user, is_ordered=False, order_number=id)
        cart_items = CartItem.objects.filter(user=request.user)
        order.is_ordered = True
        total = 0
        print('hello')
        for cart_item in cart_items:
            print(cart_item.size_variant.pk)
            print(type(cart_item.product.price))
            print(type(cart_item.quantity))
            cart_item.product.price = cart_item.product.get_product_price_by_size_id(
                cart_item.size_variant.pk)
            cart_price = cart_item.product.price
            total += (cart_item.product.price * cart_item.quantity)
        #    quantity += cart_item.quantity

        tax = (2*total)/100

        shipping = (2*total)/100
        print(type(order.order_total))
        grand_total = Decimal(str(order.order_total)) + shipping
        print('hello')

        order.order_total = grand_total
        order.save()

        payment = Payment(
            user=request.user,
            payment_id=order.order_number,
            order_id=order.order_number,
            payment_method='Cash on Delivery',
            amount_paid=order.order_total,
            status=False
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        print('dill')

        for cart_item in cart_items:
            order_product = OrderProduct()
            order_product.order_id = order.id
            order_product.payment = payment
            order_product.user_id = request.user.id
            order_product.product_id = cart_item.product_id
            order_product.variations = cart_item.size_variant
            order_product.quantity = cart_item.quantity
            order_product.product_price = cart_item.product.price
            order_product.ordered = True
            order_product.save()
            cart_item = CartItem.objects.get(id=cart_item.id)

            if cart_item.size_variant:
                product_variation = cart_item.size_variant
                print('size', cart_item.size_variant.pk)

            order_product = OrderProduct.objects.get(id=order_product.id)
            order_product.variations = product_variation
            order_product.save()

            # # Reduce quantity of variation
            print(cart_item.id)
            test = cart_item.size_variant
            print(test)
            variation = Variation.objects.get(id=cart_item.size_variant.pk)
            variation.stock -= cart_item.quantity
            variation.save()
            print('lala')
        CartItem.objects.filter(user=request.user).delete()

        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'payment': payment,
            'total': total,
            'tax': tax,
            'shipping': shipping,
        }
        return render(request, 'userside/order/order_success.html', context)
    except Exception as e:
        print(e)
        return redirect(reverse('payment_failed'))



def coupons(request):
    if request.method == 'POST':
        coupon_code = request.POST['coupon']
        grand_total = request.POST['grand_total']
        coupon_discount = 0
        
        try:
            instance = UserCoupon.objects.get(user = request.user , coupon__code = coupon_code)

            if float(grand_total) >= float(instance.coupon.min_value):
                coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
                grand_total = float(grand_total) - coupon_discount
                grand_total = format(grand_total,'.2f')
                coupon_discount = format(coupon_discount,'.2f')
                msg = 'Coupon Applied successfully'
                status = True
                instance.used = True
                instance.save()

            else:
                msg = 'this coupon is only applicable for orders more than $'+str(instance.coupon.min_value)+'\- only'
                status = False
        except:
            msg = 'coupon is not valid'
            status = False


        response ={
            'grand_total':grand_total,
            'msg': msg,
            'coupon_discount' :coupon_discount,
            'coupon_code':coupon_code,
            'status':status
        }

    return JsonResponse(response)

def cancel_order(request,id):
    if request.user.is_superadmin:
        order = Order.objects.get(order_number = id)
    else:
        order = Order.objects.get(order_number = id,user = request.user)
    order.status = "Cancelled"
    order.save()
    payment = Payment.objects.get(order_id = order.order_number)
    
    order_products = OrderProduct.objects.filter(user=request.user,order=order) 
    for order_product in order_products:
        print(order_product.variations)
        variation = Variation.objects.get(id=order_product.variations.pk)
        variation.stock += order_product.quantity
        variation.save()
        print(variation)

    profile = UserProfile.objects.get(user=request.user) 
    print(profile)
    if profile.wallet == 0:
        profile.wallet = 0.0
    if payment.status == 'True':
        print('hlo')
        print(payment.amount_paid)
        profile.wallet += payment.amount_paid
        print(profile.wallet)
        profile.save()
    
    
    payment.delete()
    if request.user.is_superadmin:
        print(type(profile.user))
        print(type(profile.user.first_name))
        messages.success(request, profile.user.first_name +'cancelled' + str(order.order_number))
        return redirect('my_orders')
    else:
        messages.success(request,'item cancelled successfully')
        return redirect('my_orders')
    
def return_order(request, id):
    
    print("loooooo")
    if request.method == 'POST':
        print('helloooooooooooooooo')
        return_reason = request.POST['return_reason']
    print(return_reason)
    order = Order.objects.get(order_number = id,user = request.user)
    order.status = "Returned"
    order.is_returned = True
    order.return_reason = return_reason
    order.save()
    payment = Payment.objects.get(order_id = order.order_number)
    print("order get")

    order_products = OrderProduct.objects.filter(user=request.user,order=order)
    for order_product in order_products: 
        # increase quantity of product variation
        print(order_product.variations)
        variation = Variation.objects.get(id=order_product.variations.pk)
        variation.stock -= order_product.quantity
        variation.save()
        print(variation)

    profile = UserProfile.objects.get(user=request.user) 
    if profile.wallet == 0:
        profile.wallet = 0.0    
    if payment.status == 'True':
        print(payment.amount_paid)
        profile.wallet += payment.amount_paid
        print(profile.wallet)
        profile.save() 

    payment.delete()              
    messages.success(request,'item returned successfully')
    return redirect('my_orders')


def wallet(request,id):
    print('hlo')
    try:
        print('hoi')
        order = Order.objects.get(user=request.user,is_ordered=False,order_number=id)
        cart_items = CartItem.objects.filter(user=request.user)
        order.is_ordered = True
        payment = Payment(
            user = request.user,
            payment_id = order.order_number,
            order_id = order.order_number,
            payment_method = 'Wallet payment', 
            amount_paid = order.order_total,
            status = 'True'
        )
        print("pathooos")
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        # Move cart item to ordered product table

        for item in cart_items:
            print("cart item",item.pk)
            order_product = OrderProduct()
            order_product.order_id = order.id
            order_product.payment = payment
            order_product.user_id = request.user.id
            order_product.product_id = item.product_id
            order_product.variations = item.size_variant
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.ordered = True
            order_product.save()
            print("cart item",item.pk)
            cart_item = CartItem.objects.get(id=item.pk)
            print(cart_item)

            if cart_item.size_variant:
                product_variation = cart_item.size_variant
                print('size', cart_item.size_variant.pk)

            order_product = OrderProduct.objects.get(id=order_product.pk)
            order_product.variations = product_variation
            order_product.save()
            
            # Reduce quantity of product

            test = cart_item.size_variant
            variation = Variation.objects.get(id=cart_item.size_variant.pk)
            variation.stock -= cart_item.quantity
            variation.save()
        
        CartItem.objects.filter(user= request.user).delete()       
        ordered_products = OrderProduct.objects.filter(order_id = order.id)  
        total = 0
        for i in ordered_products:
            total += i.product_price * i.quantity
        shipping = (2*total)/100
        tax = (2*total)/100  
        profile = UserProfile.objects.get(user=request.user)  
        profile.wallet -= order.order_total
        profile.save() 
        print('ann')
        context ={
            'order':order,
            'ordered_products':ordered_products,
            'payment':payment,
            'total':total,
            'tax':tax, 
            'profile':profile,     
            'shipping':shipping,
        }  
        return render(request,'userside/order/wallet_success.html',context)   
    
    except Exception as e:
        print(e)
        print('potti')
        return redirect(reverse('payment_failed'))
    

def payment_failed(request):
    context = {
    'method': request.GET.get('method'),
    'error_code': request.GET.get('error_code'),
    'error_description': request.GET.get('error_description'),
    'error_reason': request.GET.get('error_reason'),
    'error_payment_id': request.GET.get('error_payment_id'),
    'error_order_id': request.GET.get('error_order_id')
    }
    return render(request, 'userside/order/payment_fail.html',context)