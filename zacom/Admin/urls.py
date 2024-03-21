
from django.conf import Settings
from django.urls import path

from . import views
from products import  views as productView
from customers import  views as customView   
from offer_management import  views as offerView   
from additional_management import views as additional


urlpatterns = [
    
    path('',views.adminhome,name='adminhome'),
    path('report/<filter>',views.export_data_to_excel,name='sales-report'),
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
    path('update-orderitem-status-admin/', views.update_orderitem_status_admin, name='update_orderitem_status_admin'),
 
    path('order/return/<int:order_id>/', views.order_return, name='order-return'),
    path('return/approve/<int:return_id>/', views.order_return_approve, name='order-return-approve'),
    path('return/reject/<int:return_id>/', views.order_return_reject, name='order-return-reject'),

# coupon 
    path('Coupon/', productView.Coupon_list, name='admin-coupon'),
    path('Coupon/create', productView.Coupon_create, name='admin-create'),
    path('Coupon/edit/<int:id>/', productView.Coupon_edit, name='admin-edit'),

# offer   
    path('categoryoffer/', offerView .category_offer, name='admin-category-offer'),
    path('categoryoffer/create', offerView .create_category_offer, name='admin-create-category-offer'),
    path('categoryoffer/edit/<int:offer_id>/', offerView .edit_category_offer, name='admin-edit-category-offer'),
    path('categoryoffer/activate/<int:offer_id>/', offerView .activate_category_offer, name='activateCatOffer'),
    path('categoryoffer/deactivate/<int:offer_id>/', offerView .deactivate_category_offer, name='deactivateCatOffer'),

    path('referaloffer/',offerView.referal_offer, name='admin_referal_offer'),
    path('referaloffer/edit/<int:offer_id>',offerView.referal_offer_edit, name='admin_referal_offer_edit'),
    path('activate-category-offer/<int:offer_id>/', offerView.toggle_referral_offer, name='activate-referral-offer'),
    path('deactivate-category-offer/<int:offer_id>/', offerView.toggle_referral_offer, {'activate': False}, name='deactivate-referral-offer'),
    path('activate-referral-user/<int:user_id>/', offerView.toggle_referral_user, name='activate-referral-user'),
    path('deactivate-referral-user/<int:user_id>/', offerView.toggle_referral_user, {'activate': False}, name='deactivate-referral-user'),

    path('productoffer/', offerView.product_offer, name='admin-product-offer'),
    path('productoffer/create', offerView.create_product_offer, name='admin-create-product-offer'),
    path('productoffer/create/<int:offer_id>/', offerView.edit_product_offer, name='admin-create-product-offer'),
    path('productoffer/deactivate/<int:offer_id>/', offerView.toggle_product_offer, {'activate': False}, name='deactivate-product-offer'),
    path('productoffer/activate/<int:offer_id>/', offerView.toggle_product_offer, name='activate-product-offer'),

# banner
    path('homepage/', additional.homepage, name='homepage'),
    path('banner1/', additional.banner1, name='banner1'),
    path('banner2/', additional.banner2, name='banner2'),

]