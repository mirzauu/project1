from django.db import models
from django.utils.text import slugify
from django.db.models import UniqueConstraint, Q,F,Avg,Count
from django.urls import reverse



class Category(models.Model):
    cat_name = models.CharField(max_length=50,unique=True)
    cat_slug = models.SlugField(unique=True, blank=True,max_length=200)
    cat_image = models.ImageField(upload_to='photos/cat_image',blank=True)
    is_active = models.BooleanField(default=True)
   

    def save(self, *args, **kwargs):
        if not self.cat_slug:
            self.cat_slug = slugify(self.cat_name)
        super(Category, self).save(*args, **kwargs)
        
    def get_url(self):
        return reverse('product-by-category',args=[self.cat_slug])

    def __str__(self):
        return self.cat_name
                                                                                              


class Brand(models.Model):
    brand_name = models.CharField(max_length=50,unique=True)
    brand_image = models.ImageField(upload_to='photos/brand_image',blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name
    



#colour,storage
class Atribute(models.Model):
    atribute_name = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.atribute_name
    



#black,white and 64gb,128gb
class Atribute_value(models.Model):
    atribute = models.ForeignKey(Atribute,on_delete=models.CASCADE)
    atribute_value = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.atribute_value+"-"+self.atribute.atribute_name
    

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    product_catg = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='cate')
    product_brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    product_slug    = models.SlugField(max_length=200, blank=True, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    is_available    = models.BooleanField(default=True)
    created_date    = models.DateField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)



    def save(self, *args, **kwargs):
        product_slug_name = f'{self.product_brand.brand_name}-{self.product_name}-{self.product_catg.cat_name}'
        base_slug = slugify(product_slug_name)
        counter = Product.objects.filter(product_slug__startswith=base_slug).count()
        if counter > 0:
            self.product_slug = f'{base_slug}-{counter}'
        else:
            self.product_slug = base_slug
        super(Product, self).save(*args, **kwargs)


    def __str__(self):
        return self.product_brand.brand_name+"-"+self.product_name 




class Product_Variant(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product')
    sku_id = models.CharField(max_length=30)
    atributes = models.ManyToManyField(Atribute_value,related_name='attributes')
    max_price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    product_variant_slug = models.SlugField(unique=True, blank=True,max_length=200)
    thumbnail_image = models.ImageField(upload_to='photos/product_thumbnail',blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # objects = models.Manager()
    # variants = Product_VariantManager()
    def save(self, *args, **kwargs):
        product_variant_slug_name = f'{self.product.product_brand.brand_name}-{self.product.product_name}-{self.product.product_catg.cat_name}-{self.sku_id}'
        base_slug = slugify(product_variant_slug_name)
        counter = Product_Variant.objects.filter(product_variant_slug__startswith=base_slug).count()
        if counter > 0:
            self.product_variant_slug = f'{base_slug}-{counter}'
        else:
            self.product_variant_slug = base_slug
        super(Product_Variant, self).save(*args, **kwargs)

    
    class Meta:
        constraints = [
            UniqueConstraint(
                name='Unique skuid must be provided',
                fields=['product', 'sku_id'],
                condition=Q(sku_id__isnull=False),
            )
        ]
    def __str__(self):
        return self.product_variant_slug



    # FOR ADDITIONAL IMAGES
class Additional_Product_Image(models.Model):
    product_variant = models.ForeignKey(Product_Variant,on_delete=models.CASCADE,related_name='additional_product_images')
    image = models.ImageField(upload_to='photos/product_additional')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.image.url