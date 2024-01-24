
from django.shortcuts import get_object_or_404, render
from products.models import Category, Product,Product_Variant,Brand

# Create your views here.
 
def home(request):
    return render(request,'user_templates/home.html')


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
        products = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True)
        product_count = products.count()
        # product_varient = Product_Variant.objects.prefetch_related('atributes').filter(is_active=True)
        print(products)
        # category = categories.objects.all()
        brand = Brand.objects.all()
        print(products.query)
        
    context = { 
        'products': products,
        'product_count':  product_count,
        # 'product_varient':product_varient,
        'brand' : brand
    }
    return render(request,'user_templates/shop.html',context)
