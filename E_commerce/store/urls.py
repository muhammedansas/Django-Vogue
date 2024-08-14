from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.store,name='store'),
    path('<slug:catogary_slug>/',views.store,name='products_by_catogary'),
    path('<slug:catogary_slug>/<slug:Product_slug>/',views.product_detail,name='product_detail'),
]