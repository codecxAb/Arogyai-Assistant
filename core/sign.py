from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from . emailtesting import *



def signin(request):
    return render(request, 'signin.html')
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        email1 = request.POST['email1']
        password = request.POST['password']

        if is_valid_email(email) == False:
            messages.error(request, "Invalid Email Address!!")
            return redirect('signup')
        if email != email1:
            messages.error(request, "Email Addresses Donot Match!")
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.error(request, 'Email alr exists!!')
            return redirect('/signup')
         #password checking
        if password:
            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
                return redirect ('signup') 
            if not any(char.isupper() for char in password):
                messages.error(request, "Password must contain at least one uppercase letter.")
                return redirect ('signup')
            if not any(char.islower() for char in password):
                messages.error(request, "Password must contain at least one lowercase letter.")
                return redirect ('signup')
            if not any(char.isdigit() for char in password):
                messages.error(request, "Password must contain at least one digit.")
                return redirect ('signup')
            special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
            if not re.search(special_characters, password):
                messages.error(request, "Password must contain at least one special character.")
                return redirect ('signup')
            
            myuser = User.objects.create_user(email,password)
            myuser.is_active = False
            myuser.save()
            messages.success(request, "Your account has been successfully created. Check e-mail for activation!")

            # Email Sending
            subject = "Welcome to Arogyai"
            message = "Hello"

            
    return render(request, 'signup.html')