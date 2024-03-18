from django.shortcuts import render,redirect
from products.models import Product,Category
from .models import CategoryOffer,ReferralOffer,ReferralUser,ProductOffer
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.
@login_required(login_url='admin_login')
def category_offer(request):

    category_offer = CategoryOffer.objects.all()
    print(category_offer)

    context = {
        'category_offers':category_offer
    }
    
    return render(request,"admin_templates/category_offer.html",context)

@login_required(login_url='admin_login')
def create_category_offer(request):
    category = Category.objects.all()
    context = { 'category':category}
    if request.method == 'POST':
        offer_name           = request.POST.get('offer_name')
        expire_date          = request.POST.get('expire_date')
        categories           = request.POST.get('category')
        discount_percentage  = request.POST.get('discount_percentage')
        category_offer_image = request.FILES.get('category_offer_image')
        category             = Category.objects.get(id=categories)
        category_offer            = CategoryOffer.objects.create(
            offer_name            = offer_name,
            category              = category,
            expire_date           = expire_date,
            discount_percentage   = discount_percentage,
            category_offer_image  = category_offer_image
        )
        category_offer.save()
        return redirect('admin-category-offer')
    
    return render(request,"admin_templates/category_offer_create.html",context)
    

def edit_category_offer(request,offer_id):
    category_offer_id = offer_id
    category = Category.objects.all()
    category_offer = CategoryOffer.objects.get(id=category_offer_id)
    context = {
        'category':category,
        'category_offer':category_offer
    }
    if request.method == 'POST':
        offer_name           = request.POST.get('offer_name')
        expire_date          = request.POST.get('expire_date')
        categories           = request.POST.get('category')
        discount_percentage  = request.POST.get('discount_percentage')
        category_offer_image = request.FILES.get('category_offer_image')
        category             = Category.objects.get(id=categories)
        category_offer.offer_name            = offer_name
        category_offer.category               = category
        category_offer.expire_date            = expire_date
        category_offer.discount_percentage    = discount_percentage
        if category_offer_image:
            category_offer.category_offer_image  = category_offer_image
        category_offer.save()
        return redirect('admin-category-offer')
    return render(request, 'admin_templates/admin_templates/edit_offer_category.html', context)


def activate_category_offer(request,offer_id):
    category_offer_id = offer_id
    category = Category.objects.all()
    category_offer = CategoryOffer.objects.get(id=category_offer_id)
    category_offer.is_active=True
    category_offer.save()
    return redirect('admin-category-offer')
    

def deactivate_category_offer(request,offer_id):
    category_offer_id = offer_id
    category = Category.objects.all()
    category_offer = CategoryOffer.objects.get(id=category_offer_id)
    category_offer.is_active=False
    category_offer.save()
    return redirect('admin-category-offer')
    

########### referal offer ############

def referal_offer_edit(request,offer_id): 

    Referral_instance = ReferralOffer.objects.get(id=offer_id)
    if request.method == 'POST':
        Amount           = request.POST.get('Amount')
        expire_date          = request.POST.get('expire_date')
        User_limit           = request.POST.get('user_limit')
     
        Referral_instance.Amount=Amount
        Referral_instance.limit=User_limit
        Referral_instance.expire_date=expire_date
        Referral_instance.save()
        return redirect('admin_referal_offer')

    context={
        'referaldetail':Referral_instance
    }


    return render(request,"admin_templates/referral_offer_edit.html",context)
    
    

def referal_offer(request):

    Referral_instance = ReferralOffer.objects.get(id=1)
    all_user=ReferralUser.objects.all()

    print(Referral_instance)
    context={
        'referaldetail':Referral_instance,
        'user':all_user
    }

    return render(request,"admin_templates/referal-offer.html",context)



def toggle_referral_offer(request, offer_id, activate=True):

    referal_offer = ReferralOffer.objects.get(id=1)
    referal_offer.is_active = activate
    referal_offer.save()
    return redirect('admin_referal_offer')

def toggle_referral_user(request, user_id, activate=True):
    referral_user = ReferralUser.objects.get(id=user_id)
    referral_user.is_active = activate
    referral_user.save()
    return redirect('admin_referal_offer')

# Product offer
def product_offer(request):

    product_offer_details = ProductOffer.objects.all()
    print(product_offer_details)

    context = {
        'product_offers':product_offer_details
    }
    
    return render(request,"admin_templates/Product_offer.html",context)


def create_product_offer(request):

    product_offer_details = ProductOffer.objects.all()
    print(product_offer_details)
    product_details=Product.objects.all()
    context = { 'product':product_details}

    if request.method == 'POST':
        offer_name           = request.POST.get('offer_name')
        expire_date          = request.POST.get('expire_date')
        product_ids             = request.POST.get('product')
        print(product_ids,'ids')
        discount_percentage  = request.POST.get('discount_percentage')
        product_offer_image = request.FILES.get('category_offer_image')
        product_instances   = Product.objects.get(id=product_ids)
        print(product_instances,'ddd')
        print
        product_offer            = ProductOffer.objects.create(
            offer_name            = offer_name,
            expire_date           = expire_date,
            products           =   product_instances,
            discount_percentage   = discount_percentage,
            product_offer_image  = product_offer_image
        )
        product_offer.save()
        print('fffffffffffff')
    
    return render(request,"admin_templates/Product_offer_create.html",context)


def edit_product_offer(request,offer_id):

    product_offer_details = ProductOffer.objects.get(id=offer_id)
    print(product_offer_details)
    product_details=Product.objects.all()
    context = { 'product':product_details,
               'offer':product_offer_details,
               }

    if request.method == 'POST':
        offer_name           = request.POST.get('offer_name')
        expire_date          = request.POST.get('expire_date')
        product_ids             = request.POST.get('product')
        print(product_ids,'ids')
        discount_percentage  = request.POST.get('discount_percentage')
        product_offer_image = request.FILES.get('category_offer_image')
        product_instances   = Product.objects.get(id=product_ids)
        print(product_instances,'ddd')
        print
    
        product_offer_details.offer_name            = offer_name
        product_offer_details.expire_date           = expire_date
        product_offer_details.products              = product_instances
        product_offer_details.discount_percentage   = discount_percentage
        product_offer_details.product_offer_image   = product_offer_image
        product_offer_details.save()
        print('fffffffffffff')
        return redirect('admin-product-offer')
    
    return render(request,"admin_templates/Product_offer_edit.html",context)



def toggle_product_offer(request, offer_id, activate=True):
    referral_user = ProductOffer.objects.get(id=offer_id)
    referral_user.is_active = activate
    referral_user.save()
    return redirect('admin-product-offer')