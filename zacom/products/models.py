
from django.db import models
from django.utils.text import slugify
from django.db.models import UniqueConstraint, Q,F,Avg,Count
from django.urls import reverse
from customers.models import Account
from PIL import Image,ImageOps
from io import BytesIO
from django.core.files.base import ContentFile

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime

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
    variant_name = models.CharField( blank=True,max_length=200)
    max_price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)
    offer = models.DecimalField(max_digits=8, decimal_places=2,blank=True)
    stock = models.IntegerField()
    product_variant_slug = models.SlugField(unique=True, blank=True,max_length=200)
    thumbnail_image = models.ImageField(upload_to='photos/product_thumbnail',blank=True,default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def save(self, *args, **kwargs):
        
        # img=Image.open(self.thumbnail_image.path)

        # if img.height > 300 or img.weight > 300:
        #     output_size = (300,300)
        #     img.thumbnail(output_size)
        #     img.save(self.thumbnail_image.path)

        # if self.thumbnail_image:
        #     img = Image.open(self.thumbnail_image)
        #     max_size = (679, 679)

        # # Resize image if it exceeds max_size
        #     if img.height > max_size[0] or img.width > max_size[1]:
        #         img.thumbnail(max_size, Image.LANCZOS)

        #         if img.mode == 'RGBA':
                
        #           img = img.convert('RGB')

        #         # Save the resized image to a BytesIO buffer
        #         buffer = BytesIO()
        #         img.save(buffer, format='JPEG')
        #         buffer.seek(0)

        #         # Update the thumbnail image field with the resized image
        #         self.thumbnail_image.save(self.thumbnail_image.name, buffer, save=False) 



        
           
        # if self.thumbnail_image:
        #     img = Image.open(self.thumbnail_image.path)
        #     desired_size = (522, 522)

        #     # Create a new blank image with the desired size
        #     new_img = Image.new("RGB", desired_size, (255, 255, 255))
        #     # Paste the original image onto the new image, centered and with cropping
        #     img = ImageOps.fit(img, desired_size, Image.LANCZOS)  # Use Image.LANCZOS for high-quality downsampling

        #     # Paste the fitted image onto the new blank image
        #     x_offset = (desired_size[0] - img.size[0]) // 2
        #     y_offset = (desired_size[1] - img.size[1]) // 2
        #     new_img.paste(img, (x_offset, y_offset))

        #     # Save the new image
        #     new_img.save(self.thumbnail_image.path)

        #     print(f"Image saved: {self.thumbnail_image.path}")  # Add this line for debugging



        


        
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
    def apply_offer_discount(self):
        from offer_management.models import CategoryOffer, ProductOffer
        
        # Get the category of the product
        category = self.product.product_catg

        # Check for available offers
        category_offer = CategoryOffer.objects.filter(category=category, is_active=True).first()
        product_offers = ProductOffer.objects.filter(products=self.product, is_active=True)
        
        # If both category and product offers are present, choose the one with the highest discount
        if category_offer and product_offers:
            max_product_discount = max(product_offer.discount_percentage for product_offer in product_offers)
            if max_product_discount > category_offer.discount_percentage:
                self.sale_price = self.offer * (1 - max_product_discount / 100)
                self.save()
                return self.sale_price
            else:
                self.sale_price = self.offer * (1 - category_offer.discount_percentage / 100)
                self.save()
                return self.sale_price
        # If only category offer is present
        elif category_offer:
            self.sale_price = self.offer * (1 - category_offer.discount_percentage / 100)
            self.save()
            return self.sale_price
        # If only product offers are present
        elif product_offers:
            max_product_discount = max(product_offer.discount_percentage for product_offer in product_offers)
            self.sale_price = self.offer * (1 - max_product_discount / 100)
            self.save()
            return self.sale_price
        # If no offers are present
        else:
            self.sale_price = self.offer
            self.save()
            return self.sale_price
    # Return the discounted price after applying the discount
            
    # def apply_offer_discount(self):
    #     # Get the category of the product
    #     from offer_management.models import CategoryOffer,ProductOffer
        
    #     # Get the category of the product
    #     from products.models import Category  # Import Category here to avoid circular import
    #     category = self.product.product_catg
    #     product=self.product

    #     # Check if there's an active CategoryOffer for the category
    #     category_offer = CategoryOffer.objects.filter(category=category, is_active=True).first()
    #     product_offer = ProductOffer.objects.filter(products=product, is_active=True).first()

    #     if category_offer:
    #         # Apply the discount percentage to the sale price
            
    #         discounted = self.offer *  (category_offer.discount_percentage / 100)
    #         discounted_price=self.offer - discounted
    #         self.sale_price = discounted_price
    #         self.save()
    #         return discounted_price  # Return the discounted price after applying the discount
    #     else:
    #         self.sale_price = self.offer
    #         return self.sale_price  # Return the discounted price after applying the discount
         
    def get_product_name(self):
        return f'{self.product.product_brand} {self.product.product_name} - {", ".join([value[0] for value in self.atributes.all().values_list("atribute_value")])}'    
   
    def __str__(self):
        return self.product_variant_slug



    # FOR ADDITIONAL IMAGES
class Additional_Product_Image(models.Model):
    product_variant = models.ForeignKey(Product_Variant,on_delete=models.CASCADE,related_name='additional_product_images')
    image = models.ImageField(upload_to='photos/product_additional')
    is_active = models.BooleanField(default=True)



    def __str__(self):
        return self.image.url
    
    
################## COUPON ######################
class Coupon(models.Model):
    coupon_code         = models.CharField(max_length=100)
    is_expired          = models.BooleanField(default=False)
    discount            = models.IntegerField(default=10)
    minimum_amount      = models.IntegerField(default=400)
    max_uses            = models.IntegerField(default=10)
    expire_date         = models.DateField()
    total_coupons       = models.IntegerField(default=0)

    
    # if number of the coupon is 0 or the expired date is over set it as expired

    def save(self, *args, **kwargs):
        # Get the current date
        current_date = datetime.now().date()
        if self.is_expired==False:
            # Convert expire_date to a date object if it's a string
            if isinstance(self.expire_date, str):
                self.expire_date = datetime.strptime(self.expire_date, '%Y-%m-%d').date()
            
            # Compare expire_date with current_date
            if self.total_coupons <= 0 or self.expire_date < current_date:
                self.is_expired = True
            else:
                self.is_expired = False
        else:
             self.is_expired = True       
            
        # Save the instance
        super().save(*args, **kwargs)
    def __str__(self):
        return self.coupon_code
    

class UserCoupon(models.Model):
    user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    coupon      = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    usage_count = models.IntegerField(default=0)

    def apply_coupon(self):
        if self.coupon.is_expired:
            print('Coupon is expired')
            return False  # Coupon i
        if self.usage_count >= self.coupon.max_uses:
            print('Maximum uses reached')
            return False
        
        self.usage_count += 1
        self.save()
        print('Coupon applied successfully In UserCoupon')
        return True
    

        