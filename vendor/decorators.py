# vendor/decorators.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

def vendor_required(view_func):
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'vendor':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Only vendors are allowed to access this section.")
            return redirect('home')  
    return wrapper