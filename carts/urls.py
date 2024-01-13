from django.urls import path
from . import views


urlpatterns = [
    path('',views.cart, name = 'cart'),
    path('add_cart/<int:product_id>/',views.add_cart, name = 'add_cart'),
    path('buy_now/<int:product_id>/',views.buy_now, name = 'buy_now'),
    path('update_cart',views.update_cart, name = 'update_cart'),
    path('remove_cart_item/<int:product_id>/<int:size_id>/',views.remove_cart_item, name = 'remove_cart_item'),
    path('checkout',views.checkout, name = 'checkout'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('wishlist',views.wishlist, name='wishlist')

]