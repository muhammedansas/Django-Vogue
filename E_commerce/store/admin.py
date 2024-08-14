from django.contrib import admin
from . models import Product

# Register your models here.

class Product_Admin(admin.ModelAdmin):
    list_display = ('product_name','stock','price','product_category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}

admin.site.register(Product,Product_Admin)