from django.shortcuts import get_object_or_404, redirect, render
from .forms import *
from .models import Account
from django.contrib import messages , auth
from core.views import index    
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect(index)
    
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name = first_name, last_name = last_name , email = email , username = username , password = password)
            user.phone_number = phone_number
            user.is_active = True
            user.save()

            profile = UserProfile(user=user)
            profile.save()

            request.session['email']=email
            return redirect('sent_otp')
            

    else:
        form = RegisterationForm()
    context = {
        'form': form,

    }
    return render(request, 'userside/accounts/register.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')


    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email = email , password = password)

        if user is not None:
            auth.login(request, user)
            messages.success(request , 'You are now logged in')
            return redirect("dashboard")
        
        if not Account.objects.filter(email=email,is_active=True).exists():
            messages.error(request, "You are blocked by admin ! Please contact admin ")
            return redirect('login')
        
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'userside/accounts/login.html')

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out.')
    return redirect('login')



def sent_otp(request):
    random_num = random.randint(1000,9999)
    request.session['OTP_Key'] = random_num
    send_mail(
        "OTP AUTHENTICATING PalettePassion",
        f"{random_num} -OTP",
        settings.EMAIL_HOST_USER,
        [request.session['email']],
        fail_silently=False,
    )
    return redirect('otp_verification')

def otp_verification(request):
   if request.user.is_authenticated:
        return redirect(index)
   user=Account.objects.get(email = request.session['email'])
   if request.method=="POST":
      if str(request.session['OTP_Key']) != str(request.POST['otp']):
         print(request.session['OTP_Key'],request.POST['otp'])
         user.is_active=False
      else:
         auth.login(request,user)
         messages.success(request, "signup successful!")
         return redirect(login)
   return render(request,'userside/accounts/otp_verification.html')


def resend_otp(request):
    if request.user.is_authenticated:
        return redirect(index)
    
    email = request.session.get('email')
    print(email)
    if email is None:
        email=request.user.email
    print(email)    
    random_num = random.randint(1000, 9999)
    request.session['OTP_Key'] = random_num
    send_mail(
        "Resend OTP for PalettePassion",
        f"{random_num} -OTP",
        settings.EMAIL_HOST_USER,
        [request.session['email']],
        fail_silently=False,
    )
    messages.success(request, "OTP has been resent successfully!")
    return redirect('otp_verification')


def forgot_password(request):
    if request.method != "POST":
        return render(request, "userside/accounts/forget_password.html")
    else:
        pass1 = request.POST["re_password"]
        pass2 = request.POST["password"]
        email=request.POST["email"]
        if pass1 != pass2:
            messages.warning(request, "password not correct")
            return redirect("userside/accounts/forget_password.html")
        
        try:
            user = Account.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.warning(request, "your user email not available, plese enter a valid email")
        request.session['email']=email
        request.session['password']=pass1
        return redirect('sent_otp_forgot_password') 


def sent_otp_forgot_password(request):
   random_num=random.randint(1000,9999)
   request.session['OTP_Key']=random_num
   send_mail(
   "Send OTP for Forgot Password",
        f"{random_num} -OTP",
        settings.EMAIL_HOST_USER,
        [request.session['email']],
        fail_silently=False,
    )
   return redirect('verify_otp_forgot_password')


def verify_otp_forgot_password(request):
   user=Account.objects.get(email=request.session['email'])
   if request.method=="POST":
      if str(request.session['OTP_Key']) != str(request.POST['otp']):
         print(request.session['OTP_Key'],request.POST['otp'])
        #  user.is_active=True
      else:
         password=request.session['password']
         user.set_password(password)
         user.save()
         auth.login(request,user)
         messages.success(request, "password changed successfully!")
         return redirect('login')
   return render(request,'userside/accounts/otp_verification.html')


