from django.contrib import admin
from .models import Order,Payment,Orderproduct
# Register your models here.

admin.site.register(Order)
admin.site.register(Orderproduct)
admin.site.register(Payment)
