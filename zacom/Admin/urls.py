
from django.urls import path
from . import views


urlpatterns = [
    
    path('home/',views.adminhome,name='adminhome'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('product/',views.productdetail,name='productdetail'),
    path('deactivateproduct/<int:product_id>/',views.deactivateproduct,name='deactivateproduct'),
    path('activateproduct/<int:product_id>/',views.activateproduct,name='activateproduct'),
    


]
