from django.shortcuts import render,redirect
from products.models import Product,Category
from .models import CategoryOffer
from datetime import datetime
from django.contrib.auth.decorators import login_required

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
    