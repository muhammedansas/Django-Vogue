from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from . models import Cart,Cartitem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _cart_id(request):
    cart = f"{request.user}.{request.user.id}"
    if not cart:
        cart = f"{request.user}.{request.user.id}"  
    return cart


@login_required(login_url='login')
def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)  # to get the product
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id =    _cart_id(request)
        )
        cart.save()

    try:
        cart_item = Cartitem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item = Cartitem.objects.create(
            user=request.user,
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def decrease_item(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = Cartitem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()    
    return redirect('cart')

@login_required(login_url='login')
def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)  
    cart_item = Cartitem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def cart(request,total=0,quantity=0,cart_items=None,):
    try:
        tax = 0
        grand_total = 0
        cart_items = Cartitem.objects.filter(user=request.user,is_active=True)
        for items in cart_items:
            total += (items.product.price * items.quantity)
            quantity += items.quantity  
        tax = (2 * total)/100   
        grand_total = total + tax    
    except ObjectDoesNotExist :  
        pass    # just ignore

    context = {
        "total" : total,
        "quantity" : quantity,
        "cart_items" : cart_items,
        "tax" : tax,
        "grand_total" : grand_total
    }          
    return render(request,'cart_and_orders/cart.html',context)