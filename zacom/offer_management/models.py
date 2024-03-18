from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from products.models import Category,Product
from django.utils import timezone
from django.core.exceptions import ValidationError
from customers.models import Account
from datetime import datetime

# Create your models here.
class CategoryOffer(models.Model):
    offer_name           = models.CharField(max_length=100)
    expire_date          = models.DateField()
    category             = models.ForeignKey(Category, on_delete=models.CASCADE)  # ForeignKey relationship with Category
    discount_percentage  = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    category_offer_slug  = models.SlugField(max_length=200, unique=True)
    category_offer_image = models.ImageField(upload_to='media/category_offer/',blank=True)
    is_active            = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Automatically generate the slug from the offer name
        if not self.category_offer_slug:
            self.category_offer_slug = slugify(self.offer_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.offer_name
  
    def get_absolute_url(self):
        return reverse('category_offer_detail', kwargs={'slug': self.category_offer_slug})
    


########### referal offer ############

class ReferralOffer(models.Model):
    expire_date = models.DateField()
    Amount    = models.DecimalField(max_digits=5, decimal_places=2)
    limit     = models.IntegerField()
    is_active = models.BooleanField(default=True)
    # def save(self, *args, **kwargs):
    #     # Check if the current date is after the expire_date
    #     expire_date = datetime.strptime(self.expire_date, '%Y-%m-%d').date()
    #     if expire_date < timezone.now().date():
    #         self.is_active = False  # Set is_active to False if expired
    #     super().save(*args, **kwargs) 
            

class ReferralUser(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    count = models.IntegerField()
    code = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        referral_offer = ReferralOffer.objects.first()  # Assuming there's only one ReferralOffer object
        if referral_offer:
            if self.count >= referral_offer.limit:
                self.is_active = False
        super().save(*args, **kwargs)            

    def clean(self):
        if self.code < 1000 or self.code > 9999:
            raise ValidationError("Code must be a 4-digit integer.")

    def __str__(self):
        return str(self.code)



class ProductOffer(models.Model):
    offer_name = models.CharField(max_length=100)
    expire_date = models.DateField()
    products = models.ForeignKey(Product, related_name='product_offers',on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    product_offer_slug = models.SlugField(max_length=200, unique=True)
    product_offer_image = models.ImageField(upload_to='media/product_offer/', blank=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Automatically generate the slug from the offer name
        if not self.product_offer_slug:
            self.product_offer_slug = slugify(self.offer_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.offer_name

    def get_absolute_url(self):
        return reverse('product_offer_detail', kwargs={'slug': self.product_offer_slug})