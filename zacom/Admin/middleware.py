from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import render, redirect

class SuperuserAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if request.user.is_authenticated:
                if not request.user.is_superadmin:
                    return redirect("admin_login")
            else:
                 return redirect("admin_login")  # Redirect to the login page if user is not authenticated
        
        return self.get_response(request)
