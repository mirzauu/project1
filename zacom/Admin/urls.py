
from django.urls import path
from . import views
from products import  views as productView


urlpatterns = [
    
    path('home/',views.adminhome,name='adminhome'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('product/',views.productdetail,name='productdetail'),
    path('deactivateproduct/<int:product_id>/',views.deactivateproduct,name='deactivateproduct'),
    path('activateproduct/<int:product_id>/',views.activateproduct,name='activateproduct'),



#Product management

    path('product/edit/',productView.add_product,name='admin-product-edit'),
    path("product/create/", productView.create_product, name="product-create"),
    path("product/create/variant/", productView.create_product_with_variant, name="product-create-variant"),
    
    


]
