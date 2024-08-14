from django.contrib import admin
from . models import Account,Userprofile
from django.utils.html import format_html
# Register your models here.

admin.site.register(Account)

class Userprofileadmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:100%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile picture'
    list_display = ('thumbnail','user','city','state','country')
    
admin.site.register(Userprofile,Userprofileadmin)    