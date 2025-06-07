from django.shortcuts import render, redirect
from .decorators import vendor_required
from .forms import MyProductForm
from django.contrib import messages

@vendor_required
def create_view(request):
    if request.method == "POST":
        form = MyProductForm(request.POST, request.FILES) 
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save() 
            messages.success(request, "Product created successfully")
            return redirect("home")
        else:
            messages.error(request, "Error creating product. Please check the form.")
    else:
        form = MyProductForm()
    
    return render(request,'vendor/create_product.html',context={"form":form})

