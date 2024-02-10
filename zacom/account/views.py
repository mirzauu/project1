from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import auth,messages 
from customers.models import Account
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

# Verification mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            username = email.split('@')[0]
            # user = Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            if Account.objects.filter(username = username).exists():
                messages.error(request,'User Already Exists')
            elif Account.objects.filter(email = email).exists():
                messages.error(request,'Email Already Exists')
            elif password1 != password2:
                messages.error(request,'Passwords does not match')
            else:
                myuser = Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
                myuser.is_active    = False
                myuser.is_admin     = False
                myuser.is_superuser = False
                myuser.is_staff     = False
 
                myuser.save()

            # user activation
                current_site=get_current_site(request)
                mail_subject='please activate your account'
                message = render_to_string('user_templates/verification.html',{
                    'user': myuser,
                    'domain' : current_site,
                    'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
                    'token' : default_token_generator.make_token(myuser),
                })
                to_email = email
                send_email = EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()
                # messages.success(request,'Thank you for registering with us. We have sent you a verification email to your email address.Please verify it.')
                return redirect('/accounts/register/?command=verification&email='+email)
    return render(request, 'user_templates/login.html',)


@never_cache
def login(request):

    if request.user.is_authenticated:
        
        return redirect("home")
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user = auth.authenticate(email=email, password=password)
        check=Account.objects.get(email=email)
      
        if check.is_blocked==False:
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
           
            if user is not None :
                auth.login(request,user)
                return render(request, 'user_templates/home.html')
            
            else:
                messages.error(request,'invalid email/password') 
                return redirect ('login') 
        else:
            messages.error(request,'User is blocked') 
            return redirect ('login') 
    return render(request, 'user_templates/login.html')

@never_cache
def logout(request):
    auth.logout(request)
    return render(request, 'user_templates/home.html')


def activate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None    

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'congratulation')
        return redirect('login')
    else:
        messages.error(request,'invalid activation link')
        return redirect('register')

  