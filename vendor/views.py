from django.shortcuts import render, redirect
from .decorators import vendor_required
from store.forms import MyProductForm
from django.contrib import messages
from store.models import Product
from  django.shortcuts import get_object_or_404

from django.db.models import Q
@vendor_required
def retrive_view(request):
    if request.method == "POST":
        q = request.POST.get('q', '')
        obj = Product.objects.filter(
            Q(product_name__icontains=q) |
            Q(product_description__icontains=q)
        ).filter(user=request.user)
    else:
        obj = Product.objects.filter(user=request.user)
    no = obj.count()
    return render(request, 'vendor/index.html', context={'products': obj, 'no': no})

@vendor_required
def create_view(request):
    if request.method == "POST":
        form = MyProductForm(request.POST, request.FILES) 
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save() 
            messages.success(request, "Product created successfully")
            return redirect("vendor_dashboard")
        else:
            messages.error(request, "Error creating product. Please check the form.")
    else:
        form = MyProductForm()
    return render(request,'vendor/create.html',context={"form":form})


@vendor_required
def update_view(request,id):
    iteam=get_object_or_404(Product,id=id)
    form=MyProductForm(instance=iteam)
    if request.method=="POST":
        form=MyProductForm(request.POST,request.FILES, instance=iteam)
        if form.is_valid():
             form.save()
             messages.success(request,f"{iteam} Updated Sucessfully")
             return redirect("vendor_dashboard")
        else:
            for error in form.errors:
                messages.error(request,error)
    return render(request,'vendor/update.html',context={"form":form})

@vendor_required
def delete_view(request, id):
    item = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'Item  deleted successfully!')
        return redirect('vendor_dashboard')
    return render(request, 'delete.html')
