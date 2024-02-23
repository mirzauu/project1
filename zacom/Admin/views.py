from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from requests import request
from django.urls import reverse

from products.models import Product,Product_Variant,Brand,Category
from orders.models import Order,OrderProduct

from django.http import JsonResponse

import json
from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError, transaction

from django.http import HttpResponseBadRequest


from PIL import Image



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

def deactivate_varient(request,product_id):
    product_varient = Product_Variant.objects.get(id=product_id)
    product_varient.is_active = False
    product_varient.save()
    product= product_varient.product_id
    return redirect(reverse('product_varient_detail', kwargs={'product_id': product}))


@never_cache
def activate_varient(request,product_id):
    product_varient = Product_Variant.objects.get(id=product_id)
    product_varient.is_active = True
    product_varient.save()
    product= product_varient.product_id
    return redirect(reverse('product_varient_detail', kwargs={'product_id': product}))



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

# def category_create(request):
#     try:
#         if request.method == 'POST':
#             cat_name=request.POST['brand_title']   
#             cat_image = request.FILES.get('brand_imagee')  
        
#             brand_new=Category(cat_name=cat_name,cat_image=cat_image)
#             brand_new.save()
#             messages.success(request, 'New category Added.')
#             return redirect('admin-category')
#         else:
#             return render(request, "admin_templates/category_create.html")
#     except IntegrityError:           
#         messages.error(request, 'Sorry , it already exist')
    
def category_create(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cat_name = request.POST.get('brand_title')
            cat_image = request.FILES.get('brand_imagee')
            
            if not cat_name:
                return HttpResponseBadRequest("Category name is required")
            
            image = Image.open(cat_image)


            # Save the image
            image_path = f"{settings.MEDIA_ROOT}/photos/cat_image/{cat_image.name}"
            image.save(image_path)

            try:
                category = Category(cat_name=cat_name, cat_image=f"photos/cat_image/{cat_image.name}")
                category.save()
                messages.success(request, 'New category added.')
                return redirect('admin-category')
            except IntegrityError:
                messages.error(request, 'Category already exists.')
                return redirect('admin-category-create')
    else:

        form = ImageUploadForm()

    return render(request, "admin_templates/category_create.html" ,{'form': form})    


def category_edit(request,cat_id):
    instance = Category.objects.get(id=cat_id)


    if request.method == 'POST':
        cat_name = request.POST.get('brand_title')
        cat_image = request.FILES.get('brand_imagee')
        
        if not cat_name:
            return HttpResponseBadRequest("Category name is required")
        try:
            instance.cat_name=cat_name

            if cat_image: 
                 instance.cat_image=cat_image

            instance.save()
            messages.success(request, 'category edited.')
            return redirect('admin-category')
        except IntegrityError:
            messages.error(request, 'Category already exists.')
            return redirect('admin-category-create')
    else:
        return render(request, "admin_templates/edit-category.html",{'cat':instance})    



def orderlist(request):
    
    orders=Order.objects.all().order_by('-created_at')

   
    return render(request, "admin_templates/order_list.html",{'orders':orders})


def orderdetail(request,order_id):
    
    order = Order.objects.get(id=order_id)
    
    order_products = OrderProduct.objects.filter(order=order)
    
    grand_total=0

    for i in order_products:
        if i.order_status not in ('Cancelled Admin', 'Cancelled User'):        
            grand_total += i.grand_totol
    
      
        user=i.user
        address=i.order.shipping_address
    cleaned_string = address.replace('[', '').replace(']', '')

    # Split the string by comma and remove empty strings and 'None' values
    split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

    # Remove single quotes from each item
    cleaned_data = [item.replace("'", "") for item in split_data]


    print(cleaned_data)

    order_status = Order.ORDER_STATUS_CHOICES
   
    context={

        'orders': order,
        'order_product': order_products,
        'grand_total': grand_total,
        'user': user,
        'address': cleaned_data,
        'order_status': order_status,

    }     

   
    return render(request, "admin_templates/orders-detail.html",context)


def update_order_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            new_status = data.get('new_status')
            
            # Update the order status
            order = Order.objects.get(id=order_id)
            order.order_status = new_status
            order.save()
            order_item=OrderProduct.objects.filter(order=order)

            for i in order_item:
                i.order_status=new_status
                i.save()
                # if (new_status=='Cancelled Admin' or new_status=='Cancelled User' or new_status=='Returned User' ):
                #     product=Product_Variant.objects.filter(name__icontains=i.product_variant)
                #     print(product)


            return JsonResponse({'message': 'Order status updated successfully'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def update_orderitem_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            new_status = data.get('new_status')
            print(order_id, new_status)

            # Update the order status
            order = OrderProduct.objects.get(id=order_id)
            order.order_status = new_status
            order.save()

            return JsonResponse({'message': 'Order status updated successfully'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

        
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from image_cropping.utils import get_backend

from products.form import ImageForm
from products.models import Image, ImageFK

def add(request, image_id=None):
    image = get_object_or_404(Image, pk=image_id) if image_id else None
    form = ImageForm(instance=image)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            image = form.save()
            return HttpResponseRedirect(reverse('image_add', args=(str(image.pk),)))

    return render(request, 'includes/cropper.html', {'form': form, 'image': image})

