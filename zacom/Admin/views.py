from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from requests import request
from django.urls import reverse

from products.models import Product,Product_Variant,Brand,Category
from orders.models import Order,OrderProduct,ReturnRequest

from django.http import JsonResponse

import json
from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError, transaction

from django.http import HttpResponseBadRequest

from customers.models import Account,AdressBook
from wallet.models import Wallet,WalletTransaction
from orders.models import Payment,PaymentMethod
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


@login_required(login_url='admin_login')
def productdetail(request):
 
    if request.method == 'POST':
        selected_option = request.POST.get('selectedOption')
        print(selected_option)
        if selected_option =="All category":
             products = Product.objects.all().order_by('-id')
             product_count = products.count()
             return redirect('productdetail')
        else:
            products = Product.objects.filter(product_catg__cat_name  = selected_option)
            print(products)
            product_count = products.count()
            context= {
                'products': products,
                'products_count':product_count,
                'selectedOption':selected_option
            }
            return render(request, "admin_templates/products-list.html", context)

    else:
        products = Product.objects.all().order_by('-id')
        product_count = products.count()
        

   

    context= {
        'products': products,
        'products_count':product_count,
    }

    # return JsonResponse(context)
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


@login_required(login_url='admin_login')
def product_varient_detail(request,product_id):
    product         = Product.objects.get(id=product_id)
    product_variant = Product_Variant.objects.filter(product=product)

    context = {
        'product_variant':product_variant,
        
    }
    return render(request, "admin_templates/products-variation-list.html",context)
     

@login_required(login_url='admin_login')
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


@login_required(login_url='admin_login')  
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


   
     


@login_required(login_url='admin_login')   
def category_detail(request):

    if request.method == 'POST':
        selected_option = request.POST.get('search')
        print(selected_option)
        all_categories = Category.objects.filter(cat_name__icontains=selected_option)
    

    else:
       all_categories = Category.objects.all()


    all_categories_with_products = {}

    for category in all_categories:
        products = Product.objects.filter(product_catg=category.id)
        all_categories_with_products[category] = products

    context = {
        'all_categories': all_categories_with_products,
    }
    print(all_categories_with_products)
    return render(request, "admin_templates/category.html", context)


def category_create(request):
    try:
        if request.method == 'POST':
            cat_name=request.POST['brand_title']   
            cat_image = request.FILES.get('brand_imagee')

            print(cat_name,cat_image)  
        
            brand_new=Category(cat_name=cat_name,cat_image=cat_image)
            brand_new.save()
            messages.success(request, 'New category Added.')
            return redirect('admin-category')
        else:
            return render(request, "admin_templates/category_create.html")
    except IntegrityError:           
        messages.error(request, 'Sorry , it already exist')
        return redirect('admin-category-create')


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
    if request.method == 'POST':
        selected_option = request.POST.get('search')
        print(selected_option)
      
        orders=Order.objects.filter(order_number__icontains=selected_option).order_by('-created_at')
    else:
        orders=Order.objects.all().order_by('-created_at')

   
    return render(request, "admin_templates/order_list.html",{'orders':orders})


def orderdetail(request,order_id):
    
    order = Order.objects.get(id=order_id)
    
    order_products = OrderProduct.objects.filter(order=order)

    return_requests = []
    for order_product in order_products:
        # Step 2a: Use the related name to access the related ReturnRequest instances
        related_return_requests = order_product.return_requests.all()
        # Step 2b: Collect the related ReturnRequest instances
        return_requests.extend(related_return_requests)

    grand_total=0

    for i in order_products:
        if i.order_status not in ('Cancelled Admin', 'Cancelled User','Returned'):        
            grand_total += i.grand_totol
        user=i.user
        address=i.order.shipping_address
    cleaned_string = address.replace('[', '').replace(']', '')

    # Split the string by comma and remove empty strings and 'None' values
    split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

    # Remove single quotes from each item
    cleaned_data = [item.replace("'", "") for item in split_data]


    print(return_requests)

    order_status = Order.ORDER_STATUS_CHOICES
 
   
    context={

        'orders': order,
        'order_product': order_products,
        'grand_total': grand_total,
        'user': user,
        'address': cleaned_data,
        'order_status': order_status,
        'return_request' : return_requests,

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
            print('xxxx',order_id, new_status)
            print('---------------------------')
            
            # Update the order status
            order = OrderProduct.objects.get(id=order_id)
            print('1')

            user_id = request.user.id

            user_instance = Account.objects.get(id=user_id)
            print('2')

            wallet= Wallet.objects.get(user=user_instance)
            print('3')

            payment_order=order.order.payment
            print('4')

            method1=payment_order.payment_method
         
            print(method1)

            if new_status in ('Cancelled User', 'Cancelled Admin','Returned'):
                print('=======')
                order.order_status = new_status
                order.save()
                print('inside',method1)
                product=order.product_id
                product_instance=Product_Variant.objects.get(id=product)
                product_instance.stock += order.quantity
                product_instance.save()
                wallet.balance += order.grand_totol
                wallet.save()
                WalletTransaction.objects.create(wallet=wallet, amount=order.grand_totol, transaction_type='CREDIT')

                print('5')

                if method1=='RAZORPAY':
                    print('razropay')
                    
                else:
                    print('nop')    

            print('++++++++++++++')
            order.order_status = new_status
            order.save()
                


            return JsonResponse({'message': 'Order status updated successfully'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    


@never_cache
def order_return(request,order_id):

    instance=ReturnRequest.objects.get(order_product=order_id)
    
    context={
        'return_instance' : instance
    }
    return render(request,'admin_templates/order_return.html',context)

@never_cache
def order_return_approve(request,return_id):
    print(return_id)
    instance=ReturnRequest.objects.get(id=return_id)
    instance.status='Approved'
    instance.save()

    product_id=instance.order_product.id
    order = OrderProduct.objects.get(id=product_id)
    order.order_status = 'Returned'
    order.save()

    product=order.product_id
    product_instance=Product_Variant.objects.get(id=product)
    product_instance.stock += order.quantity
    product_instance.save()




    order_id=instance.order_product.order.id
    print(order_id)

   
    return redirect(reverse('admin-order-detail', kwargs={'order_id': order_id}))


@never_cache
def order_return_reject(request,return_id):
    instance=ReturnRequest.objects.get(id=return_id)
    instance.status='Rejected'
    instance.save()

    product_id=instance.order_product.id
    order = OrderProduct.objects.get(id=product_id)
    order.order_status = 'Returned Rejected'
    order.save()

    order_id=instance.order_product.order.id
    print(order_id)

   
    return redirect(reverse('admin-order-detail', kwargs={'order_id': order_id}))

