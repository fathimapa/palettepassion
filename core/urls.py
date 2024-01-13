from django.urls import path,re_path
from core import views
from django.conf.urls import handler404



urlpatterns = [
    path("", views.index , name= 'index'),
    path("dashboard/", views.dashboard, name = 'dashboard'),
    path("edit_profile/", views.edit_profile, name = 'edit_profile'),
    path("my_address/", views.my_address, name = 'my_address'),
    path("addAddress/", views.addAddress, name = 'addAddress'),
    path("editAddress/<int:id>/", views.editAddress, name = 'editAddress'),
    path('deleteAddress/<int:id>/', views.deleteAddress, name='deleteAddress'),
    path("change_password/", views.change_password, name = 'change_password'),
    path('deleteCheckoutAddress/<int:id>/', views.deleteCheckoutAddress, name='deleteCheckoutAddress'),
    path('AddCheckoutAddress/', views.AddCheckoutAddress, name='AddCheckoutAddress'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('my_wallet/', views.my_wallet, name='my_wallet'),
    path('my_wishlist/', views.my_wishlist, name='my_wishlist'),
    path('order_details/<int:order_id>', views.order_details, name='order_details'),
    path("invoice/<int:order_id>", views.generate_invoice_pdf,name='invoice')

    # re_path(r'^.*/$', views.error, name='error'),
]

# handler404 = 'core.views.error'
