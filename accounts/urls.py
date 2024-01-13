from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name = 'register'),
    path("login/", views.login, name = 'login'),
    path("logout/", views.logout, name = 'logout'),
    
    path("sent_otp/", views.sent_otp, name = 'sent_otp'),
    path("otp_verification/", views.otp_verification, name = 'otp_verification'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('otp_verification/forgot_password',views.verify_otp_forgot_password,name='verify_otp_forgot_password'),
    path('sent_otp/forgot_password',views.sent_otp_forgot_password,name='sent_otp_forgot_password'),
    path('resend_otp',views.resend_otp,name='resend_otp'),



]