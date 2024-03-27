from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from requests import request
from customers.models import Account,AdressBook
from orders.models import Order,OrderProduct
from orders.models import OrderProduct,Payment,PaymentMethod
from products.models import Coupon,UserCoupon
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
import random 
from django.core.exceptions import PermissionDenied
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from offer_management.models import ReferralOffer,ReferralUser
import razorpay

@receiver(pre_social_login)
def check_user_blocked(sender,request, sociallogin, **kwargs):
    user = sociallogin.user
    if user.is_blocked:
        # If user is blocked, prevent the login attempt
        raise PermissionDenied("User is blocked")
     
@never_cache 
def customer_list(request):

    all_customer=Account.objects.filter(is_superadmin=False,is_admin=False)
    context={
        'customer' : all_customer
    }
    return render(request, "admin_templates/customer_list.html",context)

@never_cache 
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
@login_required
@never_cache 
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
               'user': user_detail,
               'order_dtails' : order_dtails}

    
        
    return render(request,'dashboard/address.html',context)



@never_cache 
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


@never_cache 
def Address_edit(request,id):
    user = request.user.id
    address = AdressBook.objects.get(id=id)
    account = Account.objects.filter(id=user)
    order_dtails=OrderProduct.objects.filter(user=user).count()

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")
        locality = request.POST.get("locality")
        addres = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        address = AdressBook.objects.get(id=id)

        address.name = name
        address.phone = phone
        address.address_line_1 = addres
        address.locality = locality
        address.city = city
        address.state = state
        address.country = country
        address.pincode = pincode
        address.save()
        messages.success(request, 'Address deleted successfully.')
        return redirect('address-detail')  

    context = {
               'user':account,
               'address':address

               }    

    return render(request,'dashboard/address_edit.html',context)
    

def delete_address(request):
    address_id = request.GET.get('id')
    
    user_address = AdressBook.objects.filter(id =address_id )
    if not user_address:
        return redirect('address-detail')
    
    user_address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('address-detail')    

@never_cache 
def profile(request):
    if request.user.is_authenticated:
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
                'order_dtails':order_dtails
                }
            
        return render(request,'dashboard/profile.html',context)
    return redirect("home")
    



@never_cache 
def orders(request):
    if request.user.is_authenticated:
        user = request.user.id
        user_detail= Account.objects.get(id=user)
        order_dtails=Order.objects.filter(user=user).order_by('-created_at')
    
            
        
        context = {
                'user':user_detail,
                'order_dtails':order_dtails,
                'user_detail': user_detail,
                }
            
        return render(request,'dashboard/orders.html',context) 
    return redirect("home")                                                     


@never_cache 
def order_items(request,orderid):
    if request.user.is_authenticated:
        user = request.user.id
        user_detail= Account.objects.get(id=user)
        order_dtails=Order.objects.get(id=orderid)
        payment_status=order_dtails.payment.payment_status
        print(payment_status)
        order_products=OrderProduct.objects.filter(order=order_dtails)
        
        address=order_dtails.shipping_address

        cleaned_string = address.replace('[', '').replace(']', '')

        # Split the string by comma and remove empty strings and 'None' values
        split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

        # Remove single quotes from each item
        cleaned_data = [item.replace("'", "") for item in split_data]   
        
        context = {
                'user':user_detail,
                'order_dtails':order_dtails,
                'user_detail': user_detail,
                'address' : cleaned_data,
                'order_products' : order_products,
                "payment_status":payment_status
                }
            
        return render(request,'dashboard/icons.html',context)
    return redirect("home") 



   
   

@never_cache 
def orders_detail(request,product_id):

    if request.user.is_authenticated:
        user = request.user.id
        
        order_dtails=OrderProduct.objects.filter(user=user,id=product_id)

        order_dt=OrderProduct.objects.get(user=user,id=product_id)

        payment_method=order_dt.order.payment.payment_method

        for i in order_dtails:
                address=i.order.shipping_address

        cleaned_string = address.replace('[', '').replace(']', '')

        # Split the string by comma and remove empty strings and 'None' values
        split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

        # Remove single quotes from each item
        cleaned_data = [item.replace("'", "") for item in split_data]

        context = {
                    'order' : order_dt,
                    'address' : cleaned_data,
                    'payment' :payment_method,
                    }
        
        return render(request,'dashboard/order_detail.html',context)
    return redirect("home") 




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

    subject = "Verify Your One-Time Password (OTP) - Ashion Ecommerce Store"
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
            response_data = {
            'success': True,
            'message': 'Verified',
            }
            return JsonResponse(response_data)
    else:
        print('fffff')
        response_data = {
            'success': False,
            'message': 'Not Verified',
            }
        return JsonResponse(response_data)      

@never_cache             
def coupon(request):

    if request.user.is_authenticated:
        # all_coupon=Coupon.objects.all()
        user = request.user.id
        user_detail= Account.objects.filter(id=user)
        order_dtails=OrderProduct.objects.filter(user=user).count()
        all_coupon=Coupon.objects.all()
        available_coupon=UserCoupon.objects.filter(user=user)
    
        
        context = {
                'user':user_detail,
                'order_dtails':order_dtails,
                'coupon':available_coupon,
                'all_coupon':all_coupon
                }
            
        return render(request,'dashboard/coupon.html',context)
    return redirect("home") 

import random

def generate_four_digit_code():
    return random.randint(1000, 9999)

@never_cache 
def referral(request):

    if request.user.is_authenticated:
        # all_coupon=Coupon.objects.all()
        
        user = request.user.id  
        user_detail= Account.objects.get(id=user)
        try:
            referral_dtails=ReferralUser.objects.get(user=user_detail)
            referral_offer=ReferralOffer.objects.all().first()
            print('i')
        except ObjectDoesNotExist:
            referral_offer=ReferralOffer.objects.all().first()
            referral_code = generate_four_digit_code()
            print('isss')
            referral_dtails=ReferralUser.objects.create(user=user_detail,
                                                        count=0,
                                                        code=referral_code
                                                        )
            
            print(referral_dtails,'sds')   
            
        
        context = {
                'user_detail':user_detail,
                #    'order_dtails':order_dtails,
                #    'coupon':available_coupon
                'referral':referral_dtails,
                'referral_offer':referral_offer,
                }
            
        return render(request,'dashboard/Referral.html',context)
    
    return redirect("home") 



@never_cache 
def invoice(request,orderid):
    
    user = request.user.id
    user_detail= Account.objects.get(id=user)
    order_dtails=Order.objects.get(id=orderid)
    order_products=OrderProduct.objects.filter(order=order_dtails)
    
    address=order_dtails.shipping_address

    cleaned_string = address.replace('[', '').replace(']', '')

    # Split the string by comma and remove empty strings and 'None' values
    split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

    # Remove single quotes from each item
    cleaned_data = [item.replace("'", "") for item in split_data]   
       
    context = {
               'user':user_detail,
               'order_dtails':order_dtails,
               'user_detail': user_detail,
               'address' : cleaned_data,
               'order_products' : order_products,
               }
        
    return render(request,'dashboard/invoice.html',context)




def repay(request):
    data = json.loads(request.body)
    selected_option = data.get('payment_option')
    print(selected_option)
    order=Order.objects.get(id=selected_option)
    payment_instance=Payment.objects.get(id=order.payment.id)
    amount=payment_instance.amount_paid
    print(amount)

    client = razorpay.Client(auth=("rzp_test_vAeyohaspEahRA", "076FQiZmu52B1ODs1UWKe2HF"))
    data = { "amount":(int(float(amount))*100), "currency": "INR" }
    payment1 = client.order.create(data=data)
    payment_order_id = payment1['id']
    payment_instance.payment_order_id=payment_order_id
    payment_instance.save()
    
    return JsonResponse({'message': 'Success', 'context': payment1})      



@csrf_exempt
def paymenthandler3(request):
    print("Payment Handler endpoint reached")
    user = request.user
    if request.method == "POST":
        try:
            payment_id        = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature         = request.POST.get('razorpay_signature', '')
            print(f'1:{payment_id},2:{razorpay_order_id},3:{signature}')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            } 
            client = razorpay.Client(auth=("rzp_test_vAeyohaspEahRA", "076FQiZmu52B1ODs1UWKe2HF"))
            result = client.utility.verify_payment_signature(params_dict)

            if not result :
                return redirect('payment_failure')
            else:
                payment=Payment.objects.get(payment_order_id=razorpay_order_id)
                payment.payment_status = 'SUCCESS'
                payment.payment_id = payment_id
                payment.save()
                order = get_object_or_404(Order, payment=payment)
                return redirect('order-item',order.id)
        except Exception as e:
            print('Exception:', str(e))
            return redirect('payment_failure')
    else:
        return redirect('shop')