from django.db import models

# Create your models here.

class Banner(models.Model):
    image1 = models.ImageField(upload_to='banners/')
    image2 = models.ImageField(upload_to='banners/')
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class PromotionBanner(models.Model):
    image = models.ImageField(upload_to='promotion_banners/')
    title1 = models.CharField(max_length=100)
    title2 = models.CharField(max_length=100)
    title3 = models.CharField(max_length=100)

    def __str__(self):
        return self.title    
