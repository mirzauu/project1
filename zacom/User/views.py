
from django.shortcuts import get_object_or_404, render
from products.models import Category, Product,Product_Variant,Brand,Additional_Product_Image
from django.views.decorators.cache import never_cache
from django.db.models import Q
from offer_management.models import CategoryOffer,ProductOffer
from decimal import Decimal
from additional_management.models import Banner,PromotionBanner
# Create your views here.

def home(request):
    cate=Category.objects.all()
    pro=Product.objects.all()
    banner=Banner.objects.first()
    banner2=PromotionBanner.objects.first()
   
    dic={}
    for i in pro:
        single_product_variant = list(Product_Variant.objects.filter(product=i))
        dic[i.product_brand] = single_product_variant

    print(dic)

    context = {
        "detail": dic,
        "banner":banner,
        "banner2":banner2,
    }
    return render(request,'user_templates/home.html',context)
 

def product_detail(request, product_variant_slug):

    single_product_variant = Product_Variant.objects.select_related("product").prefetch_related("atributes").filter(product_variant_slug=product_variant_slug, is_active=True).first()
    variants = Product_Variant.objects.select_related('product').filter(product=single_product_variant.product)
    images = Additional_Product_Image.objects.filter(product_variant=single_product_variant.id).order_by('-id')
    print(images)
    
    offer = None
    offer_discount = 0

    # Retrieve category offers and product offers
    category_offers = CategoryOffer.objects.filter(is_active=True, category=single_product_variant.product.product_catg)
    product_offers = ProductOffer.objects.filter(products=single_product_variant.product, is_active=True)

    # Find the highest discount offer
    max_discount_offer = max(product_offers, key=lambda offer: offer.discount_percentage, default=None)
    if max_discount_offer and max_discount_offer.discount_percentage > (category_offers.first().discount_percentage if category_offers else 0):
        offer = max_discount_offer
    elif category_offers:
        offer = category_offers.first()

    # Calculate offer discount if an offer is available
    if offer:
        discount = (offer.discount_percentage / Decimal(100)) * single_product_variant.offer
        offer_discount = single_product_variant.offer - discount

    # Related product 
    print(single_product_variant.product.product_catg)
    related_product=Product_Variant.objects.filter(product__product_catg=single_product_variant.product.product_catg)
    print(related_product)
    context = {
        "variants": variants,
        "detail": single_product_variant,
        'image': images,
        'offer': offer,
        'offer_discount': offer_discount,
        "related_product":related_product
    }

    return render(request, 'user_templates/product-details.html', context)


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
