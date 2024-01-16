from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('shop/', views.shop,name='shop'),
    path('<slug:category_slug>/', views.shop,name='product_by_category'),

]
