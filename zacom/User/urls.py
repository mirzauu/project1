from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from customers import views as custview
from cart import views as cartview
from wallet import views as walletview
from orders import views as orderview
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.home,name='home'),
    path('shop/', views.shop,name='shop'),
    path('productdetail/<slug:product_variant_slug>/', views.product_detail, name='product_detail'),
    path('shop/<slug:product_slug>/',views.shop,name='product_by_category'),


#user dash
 
    path('address/',custview.Address_detail,name='address-detail'),
    path('address/add/',custview.Address_add,name='address-add'),
    path('address/edit/<int:id>',custview.Address_edit,name='address-edit'),
    path('delete-address/',custview.delete_address,name='deleteaddress'),
    path('profile/',custview.profile,name='profile'),
    path('order/',custview.orders,name='order'),
    path('order/detail/<int:product_id>/',custview.orders_detail,name='order-detail'),
    path('profile/sendotp/',custview.otp_sender,name='email-otp'),
    path('profile/email/verify/',custview.email_activate,name='email-verify'),
    path('profile/coupon/',custview.coupon,name='coupon-detail'),

# wallet
    path('wallet/',walletview.wallet,name='wallet'),
    path('paymenthandler2/',walletview.paymenthandler2,name='paymenthandler2'),


# cart management
    path('cart/', cartview.cart,name='cart'),
    path('cart/add/<int:product_id>/',cartview.add_cart,name='cart-add'),
    path('update_cart/<int:cart_item_id>/<int:new_quantity>/',cartview.update_cart,name='cart-update'),
    path('delete_cart_item/<int:cart_item_id>/', cartview.delete_cart_item, name='delete_cart_item'),
    path('delete_applied_coupon/<int:cart_item_id>/', cartview.delete_applied_coupon, name='delete_applied_coupon'),
    path('order-summary/',cartview.order_summary,name='order-summary'),
    path('apply_coupon/',cartview.apply_coupon,name='apply_coupon'),
 
 
# order
    path('order-address/',orderview.Address.as_view(),name='order-address'),
    path('order-review/',orderview.Review.as_view(),name='order-review'),
    path('order-payment/',orderview.Paymentt.as_view(),name='order-payment'),
    path('order-place-cod/',orderview.order_place_cod,name='order_place-cod'),
    path('order-place-wallet/',orderview.order_place_Wallet,name='order_place-wallet'),
    path('order-status/',orderview.get_current_step,name='order_status'),
    path('order-return/',orderview.orders_return,name='order_return'),
    path('paymenthander/',orderview.paymenthandler,name='paymenthander'),


]
