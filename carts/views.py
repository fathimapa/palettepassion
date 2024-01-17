from django.shortcuts import render, redirect
from store.models import *
from .models import Cart, CartItem ,Wishlist,WishlistItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from order.models import *
from core.forms import *


# Create your views here.

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        user = request.user

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=user, is_active=True)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            cart_item.product.price = cart_item.product.get_product_price_by_size_id(
                cart_item.size_variant.pk)
            cart_price = cart_item.product.price
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'userside/cart/cart.html', context)


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):

    size = request.GET.get('select_size', '').strip()
    product = Product.objects.get(pk=product_id)
    category = product.category
    category_slug = category.slug
    product_slug = product.slug
    print(size)
    try:
        print(product.product_name)
        print(product.pk)
        variant = Variation.objects.get(product_id=product_id, size=size)
        print("variant", variant)
    except Variation.DoesNotExist:
        print("this sorked")
        messages.warning(
            request, 'Variant not available, please select a variation')
        return HttpResponseRedirect(reverse('product_detail', args=(category_slug, product_slug,)))

    if variant is not None:  # Check if variant was found
        if variant.stock >= 1:
            if request.user.is_authenticated:
                try:
                    is_cart_item_exists = CartItem.objects.filter(
                        user=request.user, product=product,
                        size_variant=variant).exists()
                    print(is_cart_item_exists)
                except CartItem.DoesNotExist:
                    pass
                if is_cart_item_exists:
                    to_cart = CartItem.objects.get(
                        user=request.user, product=product, size_variant=variant)
                    variation = to_cart.size_variant
                    if to_cart.quantity < variant.stock:
                        to_cart.quantity += 1
                        to_cart.save()
                    else:
                        messages.success(request, "Product out of stock")
                else:
                    cart = Cart.objects.create(cart_id=_cart_id(request))
                    to_cart = CartItem.objects.create(
                        user=request.user,
                        product=product,
                        size_variant=variant,
                        quantity=1,
                        is_active=True,
                        cart=cart
                    )
                return redirect('cart')
            else:
                messages.success(request, "Please login to purchase")
                return redirect('login')
        else:
            messages.warning(request, 'This item is out of stock.')
            return redirect('product_detail', category_slug=category_slug, product_slug=product_slug)
    else:
        messages.warning(request, 'Variant not found.')
        return redirect('product_detail', args=(category_slug, product_slug,))


def update_cart(request):

    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        cart = int(request.POST.get('cart_id'))
        quantity = int(request.POST.get('quantity'))
        sizevariant_id = int(request.POST.get('size_variant_id'))

        cart_item = CartItem.objects.filter(
            user_id=request.user.id, product_id=prod_id, cart_id=cart, size_variant_id=sizevariant_id)
        product = Product.objects.get(pk=prod_id)

        if quantity <= 0:
            return JsonResponse({"status:Quantity can't be less than 0"})

        if product.variation_set.exists():
            variation = Variation.objects.get(
                pk=sizevariant_id, product=product)

            if variation.stock >= quantity:
                update_cart_item(request.user, cart, prod_id,
                                 quantity, variation)
                cart_items = CartItem.objects.filter(user=request.user)
                total = sum((cart_item.product.price + cart_item.size_variant.price)
                            * cart_item.quantity for cart_item in cart_items)

                tax = (2 * total) / 100
                grand_total = total + tax
                sub_total = product.get_product_price_by_size_id(
                    sizevariant_id) * quantity

                response_data = {
                    'status': 'updated Succesfully',
                    'status': 'success',
                    'total': total,
                    'tax': tax,
                    'grand_total': grand_total,
                    'sub_total': sub_total,
                }

                return JsonResponse(response_data)

            else:
                messages.warning(
                    request, 'Not enough stock for the selected variation')
                return JsonResponse({'status': 'failed'})

        # else:

        #     if product.stock < quantity:
        #         return JsonResponse({'status': 'failed', 'message': 'Not enough stock for the product'})
        #     else:
        #         update_cart_item(request.user , cart , prod_id ,quantity)

    return JsonResponse({'status': 'failed', 'message': 'Invalid request'})


def update_cart_item(user, cart_id, prod_id, quantity, variation=None):

    cart_item = CartItem.objects.get(
        product_id=prod_id, user=user, cart_id=cart_id)

    if variation:
        cart_item.size_variant = variation

    cart_item.quantity = quantity
    cart_item.save()


def remove_cart_item(request, product_id, size_id):
    product = get_object_or_404(Product, id=product_id)
    size_variation = get_object_or_404(
        Variation, id=size_id)  # get the product

    if request.user.is_authenticated:
        # to get the cartid present in the session
        cart_item = CartItem.objects.get(
            product=product, user=request.user, size_variant_id=size_variation)
    else:
        # to get the cartid present in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, cart=cart, size_variant_id=size_variation)

    cart_item.delete()

    return redirect('cart')


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = None
    grand_total = None
    address = Address.objects.filter(user=request.user)
    form = AddressForm()
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            cart_item.product.price = cart_item.product.get_product_price_by_size_id(
                cart_item.size_variant.pk)
            cart_price = cart_item.product.price
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # just ignoe

    coupons = Coupon.objects.filter(active=True)

    for item in coupons:
        try:
            coupon = UserCoupon.objects.get(user=request.user, coupon=item)
        except:
            coupon = UserCoupon()
            coupon.user = request.user
            coupon.coupon = item
            coupon.save()

    coupons = UserCoupon.objects.filter(user=request.user, used=False)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'address': address,
        'form': form,
        'coupons': coupons,

    }
    return render(request, 'userside/cart/checkout.html', context)


def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()

    else:
        cart_count = 0

    return JsonResponse({'cart_count': cart_count})


def buy_now(request, product_id):
    size = request.GET.get('select_size', '').strip()
    product = Product.objects.get(pk=product_id)
    category = product.category
    category_slug = category.slug
    product_slug = product.slug

    try:
        variant = Variation.objects.get(product_id=product_id, size=size)
    except Variation.DoesNotExist:
        messages.warning(
            request, 'Variant not available, please select a variation')
        return HttpResponseRedirect(reverse('product_detail', args=(category_slug, product_slug,)))

    if variant is not None and variant.stock >= 1:
        if request.user.is_authenticated:
            try:
                is_cart_item_exists = CartItem.objects.filter(
                    user=request.user, product=product,
                    size_variant=variant).exists()
            except CartItem.DoesNotExist:
                pass

            if is_cart_item_exists:
                to_cart = CartItem.objects.get(
                    user=request.user, product=product, size_variant=variant)
                variation = to_cart.size_variant
                if to_cart.quantity < variant.stock:
                    to_cart.quantity += 1
                    to_cart.save()
                else:
                    messages.success(request, "Product out of stock")
            else:
                cart = Cart.objects.create(cart_id=_cart_id(request))
                to_cart = CartItem.objects.create(
                    user=request.user,
                    product=product,
                    size_variant=variant,
                    quantity=1,
                    is_active=True,
                    cart=cart
                )
            # Redirect to checkout directly for Buy Now
            return redirect('checkout')
        else:
            messages.success(request, "Please login to purchase")
            return redirect('login')
    else:
        messages.warning(request, 'Variant not found or out of stock.')
        return redirect('product_detail', args=(category_slug, product_slug,))


