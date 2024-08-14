from django.urls import path
from . import views


urlpatterns = [
    path('',views.admin_panel,name='admin_panel'),
    path('<int:id>/block_user/',views.block_user,name='block_user'),
    path('admin_products/',views.admin_products,name='admin_products'),
    path('add_product/',views.add_product,name='add_product'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    path('admin_category/',views.admin_category,name='admin_category'),
    path('add_category/',views.add_category,name='add_category'),
    path('<str:slug>/edit_category/',views.edit_category,name='edit_category'),
    path("<str:slug>/delete_category/",views.delete_category,name="delete_category"),
    path('<int:id>/admin_userprofile/',views.admin_userprofile,name='admin_userprofile'),
    path('<int:id>/edit_product/',views.edit_product,name='edit_product'),
    path('admin_orders/',views.admin_orders,name='admin_orders'),
]
