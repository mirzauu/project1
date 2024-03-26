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
from collections import Counter
from django.db.models import Sum
from django.utils import timezone
import calendar
from django.db.models import Q
import pandas as pd
from datetime import timedelta
import datetime
from io import BytesIO
from django.http import HttpResponse
from django.db.models import Prefetch
from django.db.models import Count



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

def adminhome(request):
    orders=OrderProduct.objects.filter(order_status='Delivered')
    print(orders,'ffff')
    count = orders.__len__()
    revenue = OrderProduct.objects.filter(order_status='Delivered').aggregate(total_revenue=Sum('grand_totol'))['total_revenue'] or 0

    chart_month = []
    new_users = []
    orders_count= []
    for month in range(1,13):
        c = 0
        user_count = 0
        order_c = 0
        for item in orders:
            if item.created_at.month == month:
                c += item.quantity
                order_c +=1
                
        chart_month.append(c)
        for user in Account.objects.all():
            if user.date_joined.month == month:
                user_count +=1
        new_users.append(user_count)

        for order in Product_Variant.objects.all():
            if order.created_at.month == month:
                order_c +=1
        orders_count.append(order_c)

    all_orders = Order.objects.all().order_by('-created_at')

    print(chart_month, user_count, order_c)

    if request.method == 'GET':
        date = request.GET.get('date')
        order_filter = request.GET.get('order_filter')

        if order_filter and order_filter!= 'All':
            all_orders = all_orders.filter( payment__payment_status = order_filter)

        if date:
            date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
            date_datetime = datetime.strptime(str(date), '%Y-%m-%d')
            all_orders = all_orders.filter(created_at__date=date_datetime)
   
   
    delivered_orders = OrderProduct.objects.filter(order_status='Delivered')
    print(delivered_orders)
   
    product_variant_counts = (
        OrderProduct.objects
        .values('product_variant', 'images', 'product_price')
        .annotate(order_count=Count('order'))
        .order_by('-order_count')  # Order by count of orders in descending order
    )
    
    monthly_earning = monthly_earnings()
   
    products_count = Product.objects.all().__len__
    categories_count = Category.objects.all().__len__
    payment_statuses = Payment.payment_status
    context={'revenue':revenue, 'count':count, 'orders':all_orders,'date':date,'order_filter':order_filter, 'users':Account.objects.all(), 'month' : chart_month, 'new_users':new_users, 'orders_count':orders_count,'payment_statuses':payment_statuses, 'sorted_product_attributes':product_variant_counts, 'monthly_earning':monthly_earning, 'products_count':products_count, 'categories_count':categories_count}
    
    return render(request,"admin_templates/admin-home.html",context)



def monthly_earnings():
    current_year = timezone.now().year
    current_month = timezone.now().month


    # Get the number of days in the current month
    _, num_days = calendar.monthrange(current_year, current_month)

    # Calculate the start and end dates for the current month
    start_date = timezone.datetime(current_year, current_month, 1)
    end_date = timezone.datetime(current_year, current_month, num_days, 23, 59, 59)

    # Calculate the total earnings for the current month
    monthly_earnings = Order.objects.all().filter(created_at__range=(start_date, end_date)).aggregate(total_earnings=Sum('order_total'))['total_earnings'] or 0
   
    return monthly_earnings


def export_data_to_excel(request, filter):
    if filter == 'All':
        objs = OrderProduct.objects.all()
        orders = Order.objects.all()
    elif filter == 'Daily':
        today = timezone.now().date()
        objs = OrderProduct.objects.filter(order_id__created_at__date=today)
        orders = Order.objects.filter(created_at__date=today)
    elif filter == 'Weekly':
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        objs = OrderProduct.objects.filter(order_id__created_at__date__range=[start_of_week, end_of_week])
        orders = Order.objects.filter(created_at__date__range=[start_of_week, end_of_week])
    elif filter == 'Monthly':
        current_year = timezone.now().year
        current_month = timezone.now().month
        objs = OrderProduct.objects.filter(order_id__created_at__year=current_year, order_id__created_at__month=current_month)
        orders = Order.objects.filter(created_at__year=current_year, created_at__month=current_month)
    elif filter == 'Yearly':
        current_year = timezone.now().year
        objs = OrderProduct.objects.filter(order_id__created_at__year=current_year)
        orders = Order.objects.filter(created_at__year=current_year)
    
    data = []

    for obj in objs:
        order = obj.order
        payment_method = order.payment.payment_id if order.payment else '' 
        data.append({
            "Order ID": order.order_number,
            "Item ID": obj.id,
            "Product": obj.product_id,
            "Product Variant": obj.product_variant,  # Assuming this is a field in your OrderProduct model
            "Quantity": obj.quantity,
            "Price": obj.product_price,  # Assuming this is a field in your Product model
            "Payment Method": payment_method,
            "Address": order.shipping_address, 
            "Total": order.order_total,
            "Paid": order.payment.payment_status if order.payment else ''  ,  # Assuming this is a field in your Order model
            "Order Status": order.order_status,
        })

    overall_revenue = sum(order.order_total for order in orders if order.order_total)
    overall_data = {
        "Overall Revenue": overall_revenue,
    }

    df_orders = pd.DataFrame(data)
    df_overall = pd.DataFrame([overall_data])

    total_revenue = Order.objects.filter(order_status='New').aggregate(Sum('order_total'))['order_total__sum'] or 0
    total_count = Order.objects.filter(order_status='New').count() or 0
    product_count = Product.objects.all().count() or 0
    category_count = Category.objects.all().count() or 0
    monthly_revenue = total_revenue / total_count if total_count > 0 else 0

    overall_combined_data = {
        "Overall Revenue": total_revenue,
        "Total Products Available": product_count,
        "Overall Categories": category_count,
        "Monthly Income": monthly_revenue,
    }

    df_overall_combined = pd.DataFrame([overall_combined_data])

    output_buffer = BytesIO()
    with pd.ExcelWriter(output_buffer, engine='xlsxwriter') as writer:
        df_orders.to_excel(writer, sheet_name='Orders', index=False)

        worksheet_orders = writer.sheets['Orders']
        for i, col in enumerate(df_orders.columns):
            max_len = max(df_orders[col].astype(str).apply(len).max(), len(col))
            worksheet_orders.set_column(i, i, max_len)

        df_overall_combined.to_excel(writer, sheet_name='Overall', startcol=2, index=False)
        start_row_monthly_data = len(df_overall_combined) + 5
        start_col_monthly_data = len(df_overall_combined.columns) + 2
        df_monthly_data = pd.DataFrame({
            "Months": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            "Sales": [100, 150, 200, 120, 180, 250, 300, 200, 180, 220, 280, 320],
            "Products": [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160],
            "Visitors": [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600],
        })
        df_monthly_data.to_excel(writer, sheet_name='Overall', startcol=start_col_monthly_data + 5, index=False)
        worksheet = writer.sheets['Overall']
        for i, col in enumerate(df_overall_combined.columns):
            max_len = max(df_overall_combined[col].astype(str).apply(len).max(), len(col))
            worksheet.set_column(i + 2, i + 2, max_len) 

        for i, col in enumerate(df_monthly_data.columns):
            max_len = max(df_monthly_data[col].astype(str).apply(len).max(), len(col))
            worksheet.set_column(start_col_monthly_data + i, start_col_monthly_data + i, max_len)  

    output_buffer.seek(0)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_report.xlsx'
    response.write(output_buffer.getvalue())

    return response


    
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
@never_cache       
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
@never_cache
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

@never_cache
@login_required(login_url='admin_login')
def product_varient_detail(request,product_id):
    product         = Product.objects.get(id=product_id)
    product_variant = Product_Variant.objects.filter(product=product)

    context = {
        'product_variant':product_variant,
        
    }
    return render(request, "admin_templates/products-variation-list.html",context)
     
@never_cache
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

@never_cache 
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


   
     


@never_cache    
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

@never_cache 
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

@never_cache 
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


@never_cache 
def orderlist(request):
    if request.method == 'POST':
        selected_option = request.POST.get('search')
        print(selected_option)
      
        orders=Order.objects.filter(order_number__icontains=selected_option).order_by('-created_at')
    else:
        orders=Order.objects.all().order_by('-created_at')

   
    return render(request, "admin_templates/order_list.html",{'orders':orders})

@never_cache 
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

@never_cache 
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
            
            # Update the order status
            order = OrderProduct.objects.get(id=order_id)
            order_instance=Order.objects.get(id=order.order.id)
            user_id = request.user.id
            user_instance = Account.objects.get(id=user_id)
            wallet, created = Wallet.objects.get_or_create(user=user_instance)
            payment_order=order.order.payment
            method1=payment_order.payment_method
            method=str(method1)
         
            if new_status in ('Cancelled User', 'Cancelled Admin','Returned'):
                discount = order_instance.additional_discount
                total = order_instance.grand_total
                order_total = order_instance.order_total
                Total= order_total+discount
                Total-= order.grand_totol
                walletamount = order.grand_totol-discount
                order.order_status = new_status
                order.save()
                product=order.product_id
                product_instance=Product_Variant.objects.get(id=product)
                product_instance.stock += order.quantity
                product_instance.save()

                if method != 'CASH ON DELIVERY':
                    wallet.balance += walletamount
                    wallet.save()
                    WalletTransaction.objects.create(wallet=wallet, amount=walletamount, transaction_type='CREDIT',transaction_detail='Refund')

                order_instance.additional_discount=0
                order_instance.grand_total =Total
                order_instance.order_total=Total
                order_instance.save()
       
            order.order_status = new_status
            order.save()
                


            return JsonResponse({'message': 'Order status updated successfully'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

def update_orderitem_status_admin(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            new_status = data.get('new_status')
      
            # Update the order status
            order = OrderProduct.objects.get(id=order_id)
            order_instance=Order.objects.get(id=order.order.id)
            user_id = order_instance.user.id
            user_instance = Account.objects.get(id=user_id)
            wallet, created = Wallet.objects.get_or_create(user=user_instance)

     
            payment_order=order.order.payment
            method1=payment_order.payment_method
            method=str(method1)
         
            print(method1)

            if new_status in ('Cancelled User', 'Cancelled Admin','Returned'):
                discount = order_instance.additional_discount
                total = order_instance.grand_total
                order_total = order_instance.order_total
                Total= order_total+discount
                Total-= order.grand_totol
                walletamount = order.grand_totol-discount
                order.order_status = new_status
                order.save()
                product=order.product_id
                product_instance=Product_Variant.objects.get(id=product)
                product_instance.stock += order.quantity
                product_instance.save()

                if method != 'CASH ON DELIVERY':
                    wallet.balance += walletamount
                    wallet.save()
                    WalletTransaction.objects.create(wallet=wallet, amount=walletamount, transaction_type='CREDIT',transaction_detail='Refund')

                    print('5')

                order_instance.additional_discount=0
                order_instance.grand_total =Total
                order_instance.order_total=Total
                order_instance.save()
        
                
               
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



def sales(request):
   
    start_date_value = ""
    end_date_value = ""
    try:

        orders=Order.objects.filter(is_ordered = True).order_by('-created_at')
        print(" ddddddddddddddddddddddd",orders)
    
    except:
        pass
    if request.method == 'POST':
       
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_value = start_date
        end_date_value = end_date
        if start_date and end_date:
          
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

           
            orders = orders.filter(created_at__range=(start_date, end_date))
   
    context={
        'orders':orders,
        'start_date_value':start_date_value,
        'end_date_value':end_date_value
    }

    return render(request,'admin_templates/sales.html',context)