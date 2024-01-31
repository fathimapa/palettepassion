from django.urls import path
from store import views
from .views import *


urlpatterns = [
    path("", views.store , name= 'store'),
    path("search/", views.search , name= 'search'),
    path("<slug:category_slug>/", views.store , name= 'product_by_category'),
    path("<slug:category_slug>/<slug:product_slug>/", views.product_detail , name= 'product_detail'),
    path('get_price_by_size/<int:product_id>/<str:size>', views.get_price_by_size, name='get_price_by_size'),
    path('recent-products/', recently_added_products, name='recent_products'),

    
]

