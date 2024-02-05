from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from requests import request
from customers.models import Account
from django.shortcuts import get_object_or_404, redirect

from django.core.exceptions import PermissionDenied
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

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