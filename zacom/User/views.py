from django.shortcuts import render

# Create your views here.
# def index(request):
#     return render(request,'user_templates/shop.html')
def index(request):
    return render(request,'user_templates/home.html')
# def index(request):
#     return render(request,'user_templates/login.html')
def index(request):
    return render(request,'admin_templates/index.html')