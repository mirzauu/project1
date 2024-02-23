from django.contrib import admin
from .models import Payment,PaymentMethod,Order,OrderProduct

# Register your models here.

admin.site.register(Payment)
admin.site.register(PaymentMethod)
admin.site.register(Order)
admin.site.register(OrderProduct)

