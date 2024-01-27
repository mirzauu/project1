from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from requests import request

from products.models import Product,Product_Variant

from django.http import JsonResponse

# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email = email , password = password)
        if user is not None and user.is_superadmin == True:
            login(request, user)
            messages.success(request,'Successfuly Logged in')
            return redirect('adminhome')
        else:
            messages.error(request,'Bad Credentials!')
            return render(request,'admin_templates/admin-login.html')
    return render(request,'admin_templates/admin-login.html')


@login_required(login_url='admin_login')
def adminhome(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        return render(request,"admin_templates/admin-home.html")
    return redirect('home')
    # return render(request,'admin_templates/index.html')


@never_cache
@login_required(login_url='admin_login')
def adminlogout(request):
    logout(request)
    messages.success(request,'Successfuly Logged Out')
    return redirect('home')


def productdetail(request):

    if request.method == 'POST':
        selected_option = request.POST.get('selectedOption')
        if selected_option =="All category":
             products = Product.objects.all().order_by('-id')
             product_count = products.count()
        else:
            products = Product.objects.filter(product_catg__cat_name  = selected_option)
            product_count = products.count()
        
    else:
        products = Product.objects.all().order_by('-id')
        product_count = products.count()
    context= {
        'products': products,
        'products_count':product_count,
    }
    return render(request, "admin_templates/products-list.html", context)
        # products_data = [{'name': product.product_name, 'price': product.price} for product in products]
        # return render(request,"admin_templates/products-list.html", context)
        
def deactivateproduct(request,product_id):
    product = Product.objects.get(id=product_id)
    product.is_available = False
    product.save()
    return redirect('productdetail')

@never_cache
def activateproduct(request,product_id):
    product = Product.objects.get(id=product_id)
    product.is_available = True
    product.save()
    return redirect('productdetail')

def product_varient_detail(request,product_id):
    product         = Product.objects.get(id=product_id)
    product_variant = Product_Variant.objects.filter(product=product)

    context = {
        'product_variant':product_variant,
        
    }
    return render(request, "admin_templates/products-variation-list.html",context)
     

