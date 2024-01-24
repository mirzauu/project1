from django.shortcuts import render
from requests import request
from .models import Product,Product_Variant,Atribute,Category,Brand, Atribute_value,Additional_Product_Image
from Admin import urls

from .form import EditProductForm,EditProductVariantForm,CreateProductForm,CreateProductVariantForm,AddProductVariantForm
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages

# Create your views here.
def create_category(requset):
    pass


def add_product(request):
    return render(request, "admin_templates/add-product-1.html",)

    

def create_brand(requset):
    pass


def create_product(request):
    attributes = Atribute.objects.prefetch_related('atribute_value_set').filter(is_active=True)
    attribute_dict = {}
    for attribute in attributes:
        attribute_values = attribute.atribute_value_set.filter(is_active=True)
        attribute_dict[attribute.atribute_name] = attribute_values                                                                                  
    category=Category.objects.all()
    brand = Brand.objects.all()
    products =Product.objects.all()

    print(attributes)
    print(attribute_dict)
    context= {
        'category': category,
        'brand':brand,
        'products':products,
        'attribute_dict': attribute_dict,
    }   

    if request.method == "POST":
        product_title = request.POST['product_title']
        category_id = request.POST['category_id']
        brand_id = request.POST['Brand']
        description = request.POST['description']
        category = Category.objects.get(id=category_id)
        brand = Brand.objects.get(id=brand_id)
        product = Product(
            product_name = product_title,
            product_catg = category,
            product_brand= brand,
            description  = description, 
        )

        product.save()
        messages.success(request, 'Product Added.')
        return redirect('product-create')
    

    return render(request,"admin_templates/add-product-1.html",context)

       

 

def create_varient(requset):
    pass

def create_product_with_variant(request):
    attributes = Atribute.objects.prefetch_related('atribute_value_set').filter(is_active=True)
    attribute_dict = {}
    for attribute in attributes:
        attribute_values = attribute.atribute_value_set.filter(is_active=True)
        attribute_dict[attribute.atribute_name] = attribute_values  
         #to show how many atribute in fronend
        attribute_values_count = attributes.count()                                                                                 
    category=Category.objects.all()
    brand = Brand.objects.all()
    products =Product.objects.all()


    if request.method == "POST":
        product = request.POST['product']
        sku_id = request.POST['sku_id']
        max_price = request.POST['max_price']
        product_image=request.FILES.getlist('product_image')
        sale_price = request.POST['sale_price']
        stock = request.POST['stock']      
        thumbnail_image = request.POST['thumbnail_image']      
       
        #getting all atributes
        attribute_ids=[]
        for i in range(1,attribute_values_count+1):
            req_atri = request.POST.get('atributes_'+str(i))
            if req_atri != 'None':
                attribute_ids.append(req_atri)

        print(product_image)        
        print("=============================")        
 
        product_id =Product.objects.get(id=product)

    
        product_varient = Product_Variant(
            product = product_id,
            sku_id = sku_id,
            max_price  = max_price, 
            sale_price  = sale_price, 
            stock  = stock, 
            thumbnail_image = thumbnail_image
        )   
        print(product_varient.product)
        product_varient.save()
        product_varient.atributes.set(attribute_ids)
        for image in product_image:
            Additional_Product_Image.objects.create(product_variant=product_varient,image=image)
            
        print("++++++++++++++++++++++++++++++++++")

        messages.success(request, 'Product variation Added.')
        return redirect('product-create-variant')
    


    print(attributes)
    print(attribute_dict)
    context= {
        'category': category,
        'brand':brand,
        'products':products,
        'attribute_dict': attribute_dict,
    }


    return render(request,"admin_templates/add-product-1.html",context)

    