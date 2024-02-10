
from django.shortcuts import get_object_or_404, render
from products.models import Category, Product,Product_Variant,Brand,Additional_Product_Image
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def home(request):
    return render(request,'user_templates/home.html')
 
 
def product_detail(request, product_variant_slug):



    single_product_variant = (
        Product_Variant.objects.select_related("product")
        .prefetch_related("atributes")
        .filter(product_variant_slug= product_variant_slug,is_active=True))


    for i in single_product_variant:
      variants = Product_Variant.objects.select_related('product').filter(product=i.product)
      images = Additional_Product_Image.objects.filter(product_variant=i.id)
  

    context = {
        "variants": variants,
        "detail": single_product_variant,
        'image':images,
    }
    # return render(request, f"{user_page}product_detail.html", context)

    return render(request,'user_templates/product-details.html',context)

def shop(request,  product_slug=None):
    categories = None
    products = None

    if product_slug is not None:
        p=Product.objects.filter(is_available=True,product_slug=product_slug)
        products=[]
        for i in p:
            produ = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True,product=i.id)
            for j in produ:

               products.append(j)
        product_count = len(products)
    else:
        products = Product_Variant.objects.filter(is_active=True)
        p=Product.objects.filter(is_available=True)
        products=[]
        for i in p:
            produ = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True,product=i.id).first()
            products.append(produ)
        product_count = len(products)

    # Categories
    cat = Category.objects.all()
    product_detail = {}
    for category in cat:
        products_in_category = Product.objects.filter(product_catg=category.id, is_available=True)
        product_detail[category] = products_in_category

    context = {
        'products': products,
        'product_count': product_count,
        'category': product_detail,
     
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

