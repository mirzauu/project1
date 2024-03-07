from django.contrib import admin
from .models import Category,Product,Product_Variant,Atribute,Atribute_value,Brand,Coupon,UserCoupon

# Register your models here.
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('Category_name',)}
#     list_display = ('Category_name','slug')



# admin.site.register(Category,CategoryAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Product_Variant)
admin.site.register(Atribute)
admin.site.register(Atribute_value)
admin.site.register(Brand)
admin.site.register(Coupon)
admin.site.register(UserCoupon)

# class ProductAdmin(admin.ModelAdmin):
#     list_display=('product_name','price','stock','category','created_date','is_available')
#     prepopulated_fields={'slug':('product_name',)}
    


#  admin.site.register(Product,ProductAdmin)