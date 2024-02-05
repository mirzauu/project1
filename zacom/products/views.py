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



def create_product(request):

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
                                                                                     
    category=Category.objects.all()
    brand = Brand.objects.all()

    context= {
        'category': category,
        'brand':brand,
    
    }   
    print(context)
        
    return render(request,"admin_templates/add-product-1.html",context)

       


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
        thumbnail_image = request.FILES.get('thumbnail_image')  
         
       
        #getting all atributes  
        attribute_values = request.POST.getlist('attributes')
        attribute_ids = []
        varient_value=[]

        for req_atri in attribute_values:
         if req_atri != 'None': 
           a=Atribute_value.objects.filter(id=req_atri).values_list('atribute_value',flat=True)
           for i in a:
            varient_value.append(i)
            attribute_ids.append(req_atri) 
       
       
       
   

        product_id =Product.objects.get(id=product)
        product_varient = Product_Variant(
            product = product_id,
            sku_id = sku_id,
            variant_name =' '.join(varient_value),
            max_price  = max_price, 
            sale_price  = sale_price, 
            stock  = stock, 
            thumbnail_image = thumbnail_image
        )   
        
        
        product_varient.save()
        product_varient.atributes.set(attribute_ids)
        for image in product_image:
            Additional_Product_Image.objects.create(product_variant=product_varient,image=image)
        messages.success(request, 'Product variation Added.')
        return redirect('product-create-variant')
    
    context= {
        'category': category,
        'brand':brand,
        'products':products,
        'attribute_dict': attribute_dict,
    }


    return render(request,"admin_templates/add-product-varient.html",context)

def create_varient(request):
    if request.method == "POST":
        varient=request.POST['varient']
        Atribute.objects.create(atribute_name=varient)
    
    varients=Atribute.objects.all()
    context={'varients':varients}
    return render(request,"admin_templates/add-varient.html",context)



def create_varient_value(request):
    if request.method == "POST":
        varient_id=request.POST['varient_id']
        varient_value=request.POST['varient_value']
        atri=Atribute.objects.get(id=varient_id)
        atribute=Atribute_value(atribute=atri,atribute_value=varient_value)
        atribute.save()


    varients=Atribute.objects.all()
    context={'varients':varients}
    return render(request,"admin_templates/add-varient.html",context)



def edit_product_with_variant(request,product_id):
    old_product = Product_Variant.objects.get(id=product_id)
    products =Product.objects.all()

   
    attributes = Atribute.objects.prefetch_related('atribute_value_set').filter(is_active=True)
#    to get the old varient
    attr_values_list = [item['atribute_value'] for item in old_product.atributes.all().values('atribute_value')]
  

    attribute_dict = {}
    for attribute in attributes:
        attribute_values = attribute.atribute_value_set.filter(is_active=True)
        attribute_dict[attribute.atribute_name] = attribute_values  
         #to show how many atribute in fronend
        attribute_values_count = attributes.count()  

        
    if request.method == "POST":
        
        product = request.POST['product']
        sku_id = request.POST['sku_id']
        max_price = request.POST['max_price']
        product_image=request.FILES.getlist('product_image')
        sale_price = request.POST['sale_price']
        stock = request.POST['stock']      
        thumbnail_image = request.FILES.get('existing_product_images')     
       
        #getting all atributes  
        attribute_values = request.POST.getlist('attributes')
       
        attribute_ids = []
        for req_atri in attribute_values:
         if req_atri != 'None':
           attribute_ids.append(req_atri)   

        product_id =Product.objects.get(id=product)
        print('=========================')
        print(product_id)
      
        # old_product.product = product_id,65
        old_product.sku_id = sku_id
        old_product.max_price  = max_price 
        old_product.sale_price  = sale_price 
        old_product.stock  = stock 
        if thumbnail_image != None:
           old_product.thumbnail_image = thumbnail_image
        else:
           pass   
        
        
        old_product.save()
        old_product.atributes.set(attribute_ids)
        if not product_image  :
            for image in product_image:
                Additional_Product_Image.objects.create(product_variant=old_product,image=image)
        else:
            old_product.additional_product_images.all().delete()
            for image in product_image:
                Additional_Product_Image.objects.create(product_variant=old_product,image=image)
        messages.success(request, 'Product variation Added.')
        return redirect('productdetail')
     
    
    print(attribute_dict)
    context={
        "old_product":old_product,
        "products": products, 
        'attribute_dict': attribute_dict,
        'attr':attr_values_list,
    }

    return render(request,"admin_templates/edit-product-varient.html",context)

def delete_product_with_variant(request,product_id):

    instance= Product_Variant.objects.get(id=product_id)
    instance.delete()
    return render(request, "admin_templates/products-variation-list.html")

def delete_product(request,product_id):

    instance= Product.objects.get(id=product_id)
    instance.delete()
    return redirect("productdetail")

def variant_list(request):

    varients=Atribute_value.objects.all()
    context={'varients':varients}
    return render(request, "admin_templates/variant_list.html",context)


def delete_variant(request,product_id):

    instance= Atribute_value.objects.get(id=product_id)
    instance.delete()
    return redirect("variant_list")
