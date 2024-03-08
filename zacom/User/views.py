
from django.shortcuts import get_object_or_404, render
from products.models import Category, Product,Product_Variant,Brand,Additional_Product_Image
from django.views.decorators.cache import never_cache
from django.db.models import Q
from offer_management.models import CategoryOffer
from decimal import Decimal
# Create your views here.
@never_cache
def home(request):
    return render(request,'user_templates/home.html')
 
 
def product_detail(request, product_variant_slug):

    


    single_product_variant = (
        Product_Variant.objects.select_related("product")
        .prefetch_related("atributes")
        .filter(product_variant_slug= product_variant_slug,is_active=True))
    print(single_product_variant)

    for i in single_product_variant:
      variants = Product_Variant.objects.select_related('product').filter(product=i.product)
      images = Additional_Product_Image.objects.filter(product_variant=i.id)
    category_offer = None
    offer_discount=0
    category_offers = CategoryOffer.objects.filter(is_active=True,category=i.product.product_catg)
    if category_offers:
        # Iterate over the category offers
         for offer in category_offers:
            # Calculate the discount
            discount = (offer.discount_percentage / Decimal(100)) * (i.offer)
            # Calculate the discounted price
            offer_discount = i.offer - discount
            # Update category_offer to the current offer
            category_offer = offer
    

    context = {
        "variants": variants,
        "detail": single_product_variant,
        'image':images,
        'offer':category_offer,
        'offer_discount':offer_discount
    }
    # return render(request, f"{user_page}product_detail.html", context)

    return render(request,'user_templates/product-details.html',context)

def shop(request,product_slug=None):
    categories = None
    products = None
     # Get the minimum and maximum price values from the request parameters
    category_offers = CategoryOffer.objects.filter(is_active=True)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    print(min_price,max_price)

    # Filter products based on the price range if min_price and max_price are provided
    if min_price is not None and max_price is not None:
        print('1')
        p=Product.objects.filter(is_available=True)
        price_range_filter = Q(sale_price__gte=min_price, sale_price__lte=max_price)
        products=[]
        for i in p:
            produ = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True,product=i.id).filter(price_range_filter)
            print('ssssssss',produ)
            for j in produ:
               products.append(j)
        product_count = len(products)

    elif product_slug is not None:
        print('2')
        p=Product.objects.filter(is_available=True,product_catg=product_slug)
        products=[]
        for i in p:
            produ = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True,product=i.id)
            for j in produ:

               products.append(j)
        product_count = len(products)
    else:
        print('3')
        p=Product.objects.filter(is_available=True)
        products=[]
        for i in p:
            produ = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True,product=i.id).first()
            products.append(produ)
        product_count = len(products)

    # Categories
    cat = Category.objects.all()

    context = {
        
        'products': products,
        'product_count': product_count,
        'category': cat,
     
    }
    return render(request, 'user_templates/shop.html', context)

# def shop(request,category_slug=None):
#     categories = None
#     products  = None

#     if category_slug != None:
#         # categories =get_object_or_404(Category, slug=category_slug )
#         p=Product.objects.filter(product_catg__cat_slug =category_slug)
        
#         products_ls=[]
#         for i in p:

#            products = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True,product=i.id).first()

#            products_ls.append(products)
#         product_count = len(products_ls)

#         print('=====================',products_ls)

#     else:
#         p=Product.objects.filter(is_available=True)
#         products_ls=[]
#         for i in p:
#             products = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True,product=i.id).first()
#             products_ls.append(products)
#         product_count = len(products_ls)
     

#     # <--category-->
#     cat=Category.objects.all()
#     category_pr=[]
#     product_detail={}
#     for i in cat:
#         cate=Product.objects.filter(product_catg=i.id,is_available=True).all()
#         product_detail[i]=cate
    
            
           
            
#     context = { 
#         'products': products_ls,
#         'product_count': product_count,
#         'category': product_detail,
      
#     }
#     return render(request,'user_templates/shop.html',context)

# def cart(request):
#     return render(request,'user_templates/shop-cart.html')

