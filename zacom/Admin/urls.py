
from django.urls import path
from . import views
from products import  views as productView


urlpatterns = [
    
    path('home/',views.adminhome,name='adminhome'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('product/',views.productdetail,name='productdetail'),
    path('product/varient/<int:product_id>/',views.product_varient_detail,name='product_varient_detail'),
    path('deactivateproduct/<int:product_id>/',views.deactivateproduct,name='deactivateproduct'),
    path('activateproduct/<int:product_id>/',views.activateproduct,name='activateproduct'),



#Product management

  
    path("product/create/", productView.create_product, name="product-create"),
    path("product/create/variant/", productView.create_product_with_variant, name="product-create-variant"),
    path("product/edit/variant/<int:product_id>", productView.edit_product_with_variant, name="product-edit-variant"),
    path("product/delete/variant/<int:product_id>", productView.delete_product_with_variant, name="product-delete-variant"),
    path("varient/create/", productView.create_varient, name="create-variant"),
    path("varient/create/value", productView.create_varient_value, name="create-variant-value"),
    
    


]
