from django.urls import path
from store import views
from .views import *


urlpatterns = [
    path("", views.store , name= 'store'),
    path("search/", views.search , name= 'search'),
    path('create_razorpay_order/',views.create_razorpay_order,name='create_razorpay_order'),
    path("<slug:category_slug>/", views.store , name= 'product_by_category'),
    path("<slug:category_slug>/<slug:product_slug>/", views.product_detail , name= 'product_detail'),
    path('get_price_by_size/<int:product_id>/<str:size>', views.get_price_by_size, name='get_price_by_size'),
    
]

 