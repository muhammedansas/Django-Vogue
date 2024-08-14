from django.contrib import admin
from .models import catogary

# Register your models here.

class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug':('catogary_name',)}
    list_display = ('catogary_name','slug')

admin.site.register(catogary,categoryAdmin)
