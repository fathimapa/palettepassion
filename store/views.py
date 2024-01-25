from django.shortcuts import get_object_or_404, render, redirect
from store.models import *
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from category.models import category
from django.db.models import Q
from order.models import *


# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    print(min_price,max_price)

    if category_slug != None:
        categories = get_object_or_404(category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_active=True)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_active=True)
        product_count = products.count()

    
    #price filter 
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    max_page = 6

    paginator = Paginator(products,max_page )
    page_number = request.GET.get('page')
    products_final = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'products_final': products_final,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'userside/store/store.html', context)


def search(request):
    product = []
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.order_by('-created_date').filter(
                Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
    context = {
        'products_final': product,
    }
    return render(request, 'userside/store/store.html', context)


def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug, is_active=True)
        variant = Variation.objects.filter(
            product=single_product, is_active=True)

    except Product.DoesNotExist:
        # Assuming 'store' is the correct URL name for redirection
        return redirect('store')

    product_gallery = ProductGallery.objects.filter(
        product_id=single_product.id)
    context = {
        'single_product': single_product,
        'product_gallery': product_gallery,
        'variant': variant,
    }

    return render(request, 'userside/store/product_detail.html', context)


def get_price_by_size(request, product_id, size):
    product = Product.objects.get(id=product_id)
    calculated_price = product.get_product_price_by_size(size)

    print(size)

    response_data = {
        'price': calculated_price,
    }
    return JsonResponse(response_data)


