from django.contrib import admin
from .models import Category,Product

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('Category_name',)}
    list_display = ('Category_name','slug')



admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','category','created_date','is_available')
    prepopulated_fields={'slug':('product_name',)}
    


admin.site.register(Product,ProductAdmin)