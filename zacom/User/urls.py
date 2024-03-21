from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from customers import views as custview
from cart import views as cartview
from chatbot import views as chatbot
from wallet import views as walletview
from orders import views as orderview
from django.contrib.auth import views as auth_views
from Admin import views as admin


urlpatterns = [
    path('',views.home,name='home'),
    path('shop/', views.shop,name='shop'),
    path('productdetail/<slug:product_variant_slug>/', views.product_detail, name='product_detail'),
    path('shop/<slug:product_slug>/',views.shop,name='product_by_category'),
    path('adminlogin/',admin.admin_login,name='admin_login'),

#user dash
    path('address/',custview.Address_detail,name='address-detail'),
    path('address/add/',custview.Address_add,name='address-add'),
    path('address/edit/<int:id>',custview.Address_edit,name='address-edit'),
    path('delete-address/',custview.delete_address,name='deleteaddress'),
    path('profile/',custview.profile,name='profile'),
    path('order/',custview.orders,name='order'),
    path('orderitems/<int:orderid>/',custview.order_items,name='order-item'),
    path('order/detail/<int:product_id>/',custview.orders_detail,name='order-detail'),
    path('profile/sendotp/',custview.otp_sender,name='email-otp'),
    path('profile/email/verify/',custview.email_activate,name='email-verify'),
    path('profile/coupon/',custview.coupon,name='coupon-detail'),
    path('profile/referral/',custview.referral,name='referral-detail'),
    path('invoice/<int:orderid>/',custview.invoice,name='invoice'),
    path('order/repay',custview.repay,name='repay'),
    path('paymenthandler3/',custview.paymenthandler3,name='paymenthandler3'),
    


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

#  wishlist 
    path('wishlist/',cartview.wishlist,name='wishlist'),
    path('wishlist/add/<int:product_id>/',cartview.wishlist_add,name='wishlist-add'),
    path('wishlist/delete/<int:product_id>/',cartview.wishlist_remove,name='wishlist-delete'),

# order
    path('order-address/',orderview.Address.as_view(),name='order-address'),
    path('order-review/',orderview.Review.as_view(),name='order-review'),
    path('order-payment/',orderview.Paymentt.as_view(),name='order-payment'),
    path('order-place-cod/',orderview.order_place_cod,name='order_place-cod'),
    path('order-place-wallet/',orderview.order_place_Wallet,name='order_place-wallet'),
    path('order-status/',orderview.get_current_step,name='order_status'),
    path('order-return/',orderview.orders_return,name='order_return'),
    path('paymenthander/',orderview.paymenthandler,name='paymenthander'),
    path('payment_failure/',orderview.payment_failure,name='payment_failure'),
    path('success_page/<id>',orderview.success_page,name='success_page'),
    path('webhook/', chatbot.webhook_view, name='webhook'),

]
