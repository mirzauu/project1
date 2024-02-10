from django.db import models
from django.db import models
from customers.models import Account,AdressBook
from products.models import Product_Variant
from django.db.models.signals import post_save 
from django.dispatch import receiver
import datetime
# Create your models here.
class ShippingAddress(models.Model):
    #The use of two addesses is necessary. Because if there is only one address and user changes anything then the
    # shipping address will be changed.   
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    phone_number    = models.CharField(max_length=50)
    town_city       = models.CharField(max_length=100)
    street_address  = models.CharField(max_length=255)
    state           = models.CharField(max_length=50)
    country_region  = models.CharField(max_length=50)
    zip_code        = models.CharField(max_length=20)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.street_address} "


class PaymentMethod(models.Model):
    method_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.method_name

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES =(
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Success"),
        )
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    payment_order_id = models.CharField(max_length=100,null=True,blank=True)
    payment_signature = models.CharField(max_length=100,null=True,blank=True)
    payment_method = models.CharField(max_length=100,null=True,blank=True)
    amount_paid = models.CharField(max_length=30)
    payment_status= models.CharField(choices = PAYMENT_STATUS_CHOICES,max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id

class Order(models.Model):
    ORDER_STATUS_CHOICES =(
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Delivered", "Delivered"),
        ("Cancelled_Admin", "Cancelled Admin"),
        ("Cancelled_User", "Cancelled User"),
        ("Returned_User", "Returned User"),
        )
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    order_number = models.CharField(max_length=100)
    shipping_address = models.ForeignKey(AdressBook,on_delete=models.SET_NULL,null=True)
    
    # coupon_code = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    additional_discount = models.IntegerField(default=0,null=True)
    wallet_discount = models.IntegerField(default=0,null=True)
    order_note = models.CharField(max_length=100,blank=True,null=True)
    order_total = models.DecimalField(max_digits=12, decimal_places=2)
    order_status= models.CharField(choices = ORDER_STATUS_CHOICES,max_length=20,default='New')
    ip = models.CharField(max_length=50,blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def generate_order_number(self):
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        print(current_date)
        last_order = Order.objects.filter(order_number__startswith=f'ORD{current_date}').last()
        print(last_order)
        if last_order :
            sequence_number = int(last_order.order_number[-6:]) + 1
            print(sequence_number)
            print('workiing')
        else:
            print('No work')
            sequence_number = 1

        return f"ORD{current_date}{sequence_number:06d}"


    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.order_number


class OrderProduct(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product_Variant,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=12, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.order)

