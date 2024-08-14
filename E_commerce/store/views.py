from django.shortcuts import render,get_object_or_404,redirect
from . models import Product
from products_category.models import catogary

# Create your views here.

def store(request,catogary_slug=None):
    categories = None
    products = None
    product_count = None
    if catogary_slug !=None:
        categories= get_object_or_404(catogary, slug = catogary_slug)
        products = Product.objects.filter(product_category=categories,is_available = True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available = True)
        product_count = products.count()
    return render(request,'Home/store.html',{'products':products,'count':product_count})

def product_detail(request,catogary_slug,Product_slug):
    try:
        single_product = Product.objects.get(slug=Product_slug)
    except Exception as e:
        raise e

    context = {
        'single_product':single_product,
    }    
    return render(request,"Home/single_product.html",context)
