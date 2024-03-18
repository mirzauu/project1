from django.db import models
from products.models import Product_Variant ,UserCoupon
from customers.models import Account

# Create your models here.
class Cart(models.Model):
    
    cart_id = models.CharField(max_length=250,blank=True)
    coupon = models.ForeignKey(UserCoupon,on_delete=models.SET_NULL,null=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product_Variant,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
         return self.product.sale_price * self.quantity
    
    def __str__(self):
        return str(self.product)
    

class Wishlist(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product_Variant)
 

    def __str__(self):
        return f"{self.user.username}'s Wishlist" 