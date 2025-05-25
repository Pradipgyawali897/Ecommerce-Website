from django.shortcuts import render, redirect
from .models import Account
from django.contrib.auth import login,logout,authenticate
from .forms import RegistrationForm
from django.contrib import messages

#verification dependencies
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = form.save(commit=False)
            user.is_active = False  # Wait for email verification
            user.save()

            current_site = get_current_site(request)
            mail_subject = f"Dear {user.username}, Please activate your account"
            message = render_to_string('accounts/activate_account_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            email_message = EmailMessage(mail_subject, message, to=[email])
            try:
                email_message.send()
                messages.success(request, "Successfully registered. Please check your email to activate your account.")
            except:
                messages.error(request, "Error sending activation email.")
            return redirect('login')
    else:
        form = RegistrationForm()
        messages.info(request, "Enter the regional code in phone number")

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Logged in")
            return redirect('home')  
        else:
            messages.error(request,"Error in login")
            return render(request, 'accounts/login.html', {'error': 'Invalid email or password'})

    return render(request, 'accounts/login.html')



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request,"Logout sucessfull")
        return redirect('home')
    return render(request,'accounts/logout.html')

def activate(request):
    return 