from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from requests import request
from customers.models import Account,AdressBook
from django.shortcuts import get_object_or_404, redirect

from django.core.exceptions import PermissionDenied
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.http import JsonResponse
import json


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
    address = AdressBook.objects.filter(user=user)
   
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

    context = {'adress': address}
    print('xxx',user,address)

    
        
    return render(request,'dashboard/address.html',context)

# def Address_add(request):
#     all_addresses = AdressBook.objects.all()
#     address_data = [{'id': address.id, 'name': address.name} for address in all_addresses]
#     return JsonResponse({'addresses': address_data})

from django.http import JsonResponse

def Address_add(request):
    user = request.user.id
    address = AdressBook.objects.filter(user=user)
    account=Account.objects.get(id=user)
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        pincode = request.POST.get("pincode")
        locality = request.POST.get("locality")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        print('=====ccccccccccccccccccccccccccccccccccc=======================================')
        address_new=AdressBook(user=account,name=name,phone=phone,address_line_1=address,locality=locality,city=city,state=state,country=country,pincode=pincode)
        print('fff',address_new)
        address_new.save()
        print('fff',city)
        print('============================================')


        return JsonResponse({"message": "Address submitted successfully!"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
