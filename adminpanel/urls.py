from django.urls import path
from . import views
from .views import *
from store.admin import *
from .view import (
    ProductList, ProductCreate, ProductUpdate,
    delete_image,
)

urlpatterns = [

    #-------------------------Admin Management Urls-------------------------#

    path("admin_signin/", views.admin_signin, name = 'admin_signin'),
    path("admin_dashboard/", views.admin_dashboard, name = 'admin_dashboard'),
    path("admin_logout/", views.admin_logout, name = 'admin_logout'),
    

    #-------------------------User Management Urls-------------------------#

    path("admin_user_management/", views.admin_user_management, name = 'admin_user_management'),
    path("create_user/", views.create_user_from_admin, name = 'create_user_from_admin'),
    path('admn_users_block_unblock', views.admn_users_block_unblock, name='admn_users_block_unblock'),

    #-------------------------cstegory Management Urls-------------------------#

    path("admin_category_management/", views.admin_category_management, name = 'admin_category_management'),
    path('add_category/', views.add_category, name='add_category'),
    path('admn_category_block_unblock', views.admn_category_block_unblock, name='admn_category_block_unblock'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='update_category'),


    #-------------------------Product Management Urls-------------------------#

    path("admin_product_management/",  ProductList.as_view(), name = 'admin_product_management'),
    path('create/', ProductCreate.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdate.as_view(), name='update_product'),
    path('delete-image/<int:pk>/', delete_image, name='delete_image'),
    path('admn_product_block_unblock', views.admn_product_block_unblock, name='admn_product_block_unblock'),
    # path('add_product/', views.add_product, name='add_product'),
    # path('edit_product/<int:id>/', views.edit_product, name='edit_product'),

    #-------------------------Variation Management Urls-------------------------#
    path('variationlist/', VariationList.as_view(), name='variationlist'),
    path('create_variation/',VariationCreateVeiw.as_view(),name='create_variation'),
    path('variation/<int:pk>/update/',VariationUpdateView.as_view(),name='update_variation'),
    path('variation_block_or_unblock_view/', VariationBlockOrUnblockView.as_view(), name='variation_block_or_unblock_view'),

    #-------------------------Order Management Urls-------------------------#
    path('orderlist/', OrderList.as_view(), name='orderlist'),
    path('update_order/<int:pk>/',OrderUpdateView.as_view(),name='update_order'),

    #-------------------------Coupon Management Urls-------------------------#
    path('CouponList/', CouponList.as_view(), name='CouponList'),
    path('create_coupon/',CouponCreateView.as_view(),name='create_coupon'),
    path('coupon/<int:pk>/update/',CouponUpdateView.as_view(),name='update_coupon'),
    path('coupon_block_unblock/',CouponBlockOrUnblockView.as_view(),name='CouponBlockOrUnblockView'),


    #-------------------------Banner Management Urls-------------------------#
    path('BannerList/', BannerList.as_view(), name='BannerList'),
    path('create_banner/',BannerCreateView.as_view(),name='create_banner'),
    path('banner/<int:pk>/update/',BannerUpdateView.as_view(),name='update_banner'),
    path('banner_block_unblock/',BannerBlockOrUnblockView.as_view(),name='BannerBlockOrUnblockView'),


    #-------------------------Sales Report Urls-------------------------#

    path('salesReport/', views.salesReport,name='salesReport'),
    path('salesReportMonth/<int:id>', views.salesReportMonth,name='salesReportMonth'),
    path('salesReportYear/<int:id>', views.salesReportYear,name='salesReportYear'),

]