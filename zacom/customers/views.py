from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from requests import request
from customers.models import Account,AdressBook
from orders.models import Order,OrderProduct
from orders.models import OrderProduct
from django.shortcuts import get_object_or_404, redirect
import random 
from django.core.exceptions import PermissionDenied
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist



@receiver(pre_social_login)
def check_user_blocked(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    if user.is_blocked:
        # If user is blocked, prevent the login attempt
        raise PermissionDenied("User is blocked")
     

def customer_list(request):

    all_customer=Account.objects.filter(is_superadmin=False,is_admin=False)
    context={
        'customer' : all_customer
    }
    return render(request, "admin_templates/customer_list.html",context)

def customer_details(request):
    user_id = request.GET.get('userId')
    user = Account.objects.get(id=user_id)
    address = AdressBook.objects.filter(user=user.id,is_default=True).first()
    ordered_products = OrderProduct.objects.filter(user=user,ordered=True).order_by('-created_at')

    context={
        "user":user,
        'address':address,
        'ordered_products':ordered_products,
        'ordered_products_count':ordered_products.count()
    }
    return render(request,'admin_templates/customer-detail.html',context)



def activate_customer(request, user_id):
    current = get_object_or_404(Account, id=user_id)
    current.is_blocked = True
    current.save()
    return redirect('customer-list')

@never_cache
def deactivate_customer(request, user_id):
    current = get_object_or_404(Account, id=user_id)
    current.is_blocked = False
    current.save()
    return redirect('customer-list')


# address

def Address_detail(request):
    user = request.user.id
    address = AdressBook.objects.filter(user=user).order_by('-created_at')
    user_detail= Account.objects.filter(id=user)
    order_dtails=OrderProduct.objects.filter(user=user).count()

   
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_address_id = data.get('addressId')

        # print(selected_address_id)
        if selected_address_id:
            try:
                selected_address = AdressBook.objects.get(pk=selected_address_id)
                selected_address.is_default = True
                selected_address.save()

                # Update other addresses to set is_default=False
                AdressBook.objects.filter(user=user).exclude(pk=selected_address_id).update(is_default=False)

                return JsonResponse({'success': True, 'message': 'Address set as default successfully'})
            except AdressBook.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Selected address not found'})
        else:
            return JsonResponse({'success': False, 'message': 'No address ID provided'})

    context = {'adress': address,
               'user':user_detail,
               'order_dtails':order_dtails}

    
        
    return render(request,'dashboard/address.html',context)

# def Address_add(request):
#     all_addresses = AdressBook.objects.all()
#     address_data = [{'id': address.id, 'name': address.name} for address in all_addresses]
#     return JsonResponse({'addresses': address_data})



def Address_add(request):
    user = request.user.id
    address = AdressBook.objects.filter(user=user)
    account = Account.objects.get(id=user)
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")
        locality = request.POST.get("locality")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
   
        address_new=AdressBook(user=account,name=name,phone=phone,address_line_1=address,locality=locality,city=city,state=state,country=country,pincode=pincode)

        address_new.save()
    
       

        return JsonResponse({"message": "Address submitted successfully!"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
def delete_address(request):
    address_id = request.GET.get('id')
    
    user_address = AdressBook.objects.filter(id =address_id )
    if not user_address:
        return redirect('address-detail')
    
    user_address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('address-detail')    

def profile(request):
    user = request.user.id
    user_detail= Account.objects.get(id=user)
    order_dtails=OrderProduct.objects.filter(user=user).count()
    if request.method == "POST":
        first_name = request.POST.get("First_name")
        last_name = request.POST.get("Last_name")
        username = request.POST.get("Username")
        phone = request.POST.get("Phone")

        user_detail.first_name = first_name
        user_detail.last_name = last_name  
        user_detail.username = username
        user_detail.phone_number = phone
        
       
    context = {
               'user':user_detail,
               'order_dtails':order_dtails}
        
    return render(request,'dashboard/profile.html',context)



def orders(request):
    
    user = request.user.id
    user_detail= Account.objects.get(id=user)
    order_dtails=OrderProduct.objects.filter(user=user).order_by('-created_at')
   
        
       
    context = {
               'user':user_detail,
               'order_dtails':order_dtails,
               'user_detail': user_detail,
               }
        
    return render(request,'dashboard/orders.html',context)



   
   


def orders_detail(request,product_id):
    user = request.user.id

    
    draft_order=Order.objects.filter(user=user).order_by('-created_at').first()
    
    order_dtails=OrderProduct.objects.filter(user=user,id=product_id)
        
    
        
    context = {
                'order_dtails' : draft_order,
                # 'address' : address,
                'order_product' : order_dtails
                }

  
        
    return render(request,'dashboard/order_detail.html',context)





def otp_sender(request):
    data = json.loads(request.body)
    email = data.get('email')
    print(email)

    randomotp = str(random.randint(100000, 999999))

    request.session['storedotp']    = randomotp
    request.session['storedemail']  = email
    # request.session['storedotp'].set_expiry(300)
    # request.session['storedemail'].set_expiry(300)
    request.session.modified = True

    subject = "Verify Your One-Time Password (OTP) - Home Decor Ecommerce Store"
    sendermail = "noreply@homedecorestore.com"
    otp = f"Dear User,\n\n Your One-Time Password (OTP) for verification is: {randomotp}\n\nThank you for choosing Home Decor Ecommerce Store."
    send_mail(subject,otp,sendermail,[email])
    response_data = {
            'success': True,
            'message': 'Cart updated successfully',
        }
    return JsonResponse(response_data)


def email_activate(request):
    data = json.loads(request.body)
    otp = data.get('otp')
    print(otp)
    user=request.user.id

    storedotp=request.session['storedotp']
    storedemail = request.session['storedemail']
    print('session',storedotp)
    print('email',storedemail)
    if otp == storedotp:
            user_instance = Account.objects.get(id=user)
            user_instance.email=storedemail
            user_instance.save()
            print('mmmmmm',user_instance)
    else:
        print('oooooooo')        
            

    response_data = {
            'success': True,
            'message': 'verified',
        }
    return JsonResponse(response_data)