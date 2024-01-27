
from django.shortcuts import get_object_or_404, render
from products.models import Category, Product,Product_Variant,Brand,Additional_Product_Image
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def home(request):
    return render(request,'user_templates/home.html')
 
def product_detail(request,sku_id):



    single_product_variant = (
        Product_Variant.objects.select_related("product")
        .prefetch_related("atributes")
        .filter(sku_id=sku_id,is_active=True))


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


def shop(request,category_slug=None):
    categories = None
    products  = None

    if category_slug != None:
        categories =get_object_or_404(Category, slug=category_slug )
        products = Product_Variant.objects.all()

        product_count = products.count()
        # product_varient = Product_Variant.objects.fil.values_list('atributes__atribute_value')
        brand = Brand.objects.all()
    else:
        p=Product.objects.filter(is_available=True)
        ls=[]
        for i in p:
            products = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True,product=i.id).first()
            ls.append(products)



        product_count = len(ls)
        # product_varient = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True)
        # category = categories.objects.all()
        brand = Brand.objects.all()

        # <--category-->
        cat=Category.objects.all()
        category_pr=[]
        for i in cat:
            cate=Product.objects.filter(product_catg=i.id)
            category_pr.append(cate)
        print("===============")
        print(cate)
        
    context = { 
        'products': ls,
        'product_count':  product_count,
        'category': cat,
        'brand' : brand
    }
    return render(request,'user_templates/shop.html',context)

def cart(request):
    return render(request,'user_templates/shop-cart.html')