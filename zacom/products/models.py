from django.db import models

# Models for products

# class product(models.Model):
#     title=models.CharField(max_length=100)
#     price=models.FloatField()
#     description=models.TextField()
#     image=models.ImageField(upload_to='/media')
#     priority=models.IntegerField(default=0)

class Category(models.Model):
    Category_name   = models.CharField(max_length=50 , unique=True)
    slug            = models.SlugField(max_length=100 , unique=True)
    description     = models.CharField(max_length=255)
    cat_image       = models.ImageField(upload_to='media/photos/categories',blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural='categories'


    def __str__ (self):
        return self.Category_name


class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.product_name