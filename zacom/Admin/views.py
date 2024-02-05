from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from requests import request

from products.models import Product,Product_Variant,Brand,Category

from django.http import JsonResponse

# Create your views here.
@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        return render(request,"admin_templates/admin-home.html")
    else:
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

@never_cache
@login_required(login_url='admin_login')
def adminhome(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        return render(request,"admin_templates/admin-home.html")
    return redirect('admin_login')
    # return render(request,'admin_templates/index.html')


@never_cache
@login_required(login_url='admin_login')
def adminlogout(request):
    logout(request)
    messages.success(request,'Successfuly Logged Out')
    return redirect('admin_login')


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
     

def Brand_detail(request):

    all_brand=Brand.objects.all()
    all_brand_product={}
    for i in all_brand:
       product=Product.objects.filter(product_brand=i.id)
       all_brand_product[i]=product
    #    all_brand_product.append(product)

    count1=len(all_brand_product)   
    print(all_brand_product)
    print(count1)


    context={
        'all_brand': all_brand_product,
    }
    return render(request, "admin_templates/brands.html",context)
     
def Brand_create(request):

    if request.method == 'POST':
        brand_name=request.POST['brand_title']   
        brand_image1 = request.FILES.get('brand_imagee')  
       
        print('=====================')
        print(brand_image1)
        brand_new=Brand(brand_name=brand_name,brand_image=brand_image1)
        brand_new.save()
        messages.success(request, 'New brand Added.')
        return redirect('admin-brand')
    else:
        return render(request, "admin_templates/brand_create.html")


   
     
def category_detail(request):

    all_brand=Category.objects.all()
    all_brand_product={}
    for i in all_brand:
       product=Product.objects.filter(product_catg=i.id)
       all_brand_product[i]=product
    #    all_brand_product.append(product)

    count1=len(all_brand_product)   
    print(all_brand_product)
    print(count1)


    context={
        'all_brand': all_brand_product,
    }
    return render(request, "admin_templates/category.html",context)

def category_create(request):

    if request.method == 'POST':
        cat_name=request.POST['brand_title']   
        cat_image = request.FILES.get('brand_imagee')  
       
        print('=====================')
        print(cat_image)
        brand_new=Category(cat_name=cat_name,cat_image=cat_image)
        brand_new.save()
        messages.success(request, 'New category Added.')
        return redirect('admin-category')
    else:
        return render(request, "admin_templates/category_create.html")