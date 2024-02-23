
from django.conf import Settings
from django.urls import path

from . import views
from products import  views as productView
from customers import  views as customView


urlpatterns = [
    
    path('',views.admin_login,name='admin_login'),
    path('home/',views.adminhome,name='adminhome'),
    path('adminllogout/',views.adminlogout,name='admin_logout'),
    path('product/',views.productdetail,name='productdetail'),
    path('product/varient/<int:product_id>/',views.product_varient_detail,name='product_varient_detail'),
    path('deactivateproduct/<int:product_id>/',views.deactivateproduct,name='deactivateproduct'),
    path('activateproduct/<int:product_id>/',views.activateproduct,name='activateproduct'),
    path('deactivate/<int:product_id>/',views.deactivate_varient,name='deactivatevarient'),
    path('activate/<int:product_id>/',views.activate_varient,name='activatevarient'),



#Product management

  
    path("product/create/", productView.create_product, name="product-create"),
    path("product/edit/<int:product_id>", productView.edit_product, name="product-edit"),
    path("product/delete/<int:product_id>", productView.delete_product, name="product-delete"),
    path("product/create/variant/", productView.create_product_with_variant, name="product-create-variant"),
    path("product/edit/variant/<int:product_id>", productView.edit_product_with_variant, name="product-edit-variant"),
    path("product/delete/variant/<int:product_id>", productView.delete_product_with_variant, name="product-delete-variant"),

#Varient management  
 
    path("varient/create/", productView.create_varient, name="create-variant"),
    path("varient/create/value", productView.create_varient_value, name="create-variant-value"),
    path("varient/list/", productView.variant_list, name="variant_list"),
    path("varient/delete/<int:product_id>", productView.delete_variant, name="varient-delete"),
    
# Brand 
    path("brand/", views.Brand_detail, name="admin-brand"),
    path("brand/create/", views.Brand_create, name="admin-brand-create"),

# customer
    path("customer/list/", customView.customer_list, name="customer-list"),
    path('customer/activate/<int:user_id>/',customView.deactivate_customer,name='deactivate-customer'),
    path('customer/deactivate/<int:user_id>/',customView.activate_customer,name='activate-customer'),
    path('customer-details/', customView.customer_details, name='customer_details'),

#  category  
    path("category/", views.category_detail, name="admin-category"),
    path("category/create/", views.category_create, name="admin-category-create"),
    path("category/edit/<int:cat_id>/", views.category_edit, name="admin-category-edit"),

# order
    path("order/list/", views.orderlist, name="admin-order-list"),
    path("order/detail/<int:order_id>/", views.orderdetail, name="admin-order-detail"),
    path('update-order-status/', views.update_order_status, name='update_order_status'),
    path('update-orderitem-status/', views.update_orderitem_status, name='update_orderitem_status'),
    path('up/', views.add, name='rderitem_status'),


]

