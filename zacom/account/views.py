from django.shortcuts import render,redirect
from django.contrib import auth,messages 
from customers.models import Account
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print('h')
        if form.is_valid():
            print('hi')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.phone_number=phone_number
            user.save()
    else:
        form = ReferenceError()     
    context= {
        'form': form,
    }
    return render(request, 'user_templates/login.html',context)



def login(request):

    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request,user)
            print('if')  
            return render(request, 'user_templates/home.html')
        else:
            messages.error(request,'invalid')
            print('else')  
            return redirect ('login') 
    return render(request, 'user_templates/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    return render(request, 'user_templates/home.html')