from django.shortcuts import render,redirect
from cart.models import Cartitem
from .forms import Orderform
from .models import Order,Payment
import datetime
import json
from django.contrib import messages

# Create your views here.

def place_order(request,grand_total=0,tax=0):
    order=None
    current_user = request.user

    #if the  cart count is less than or equal to 0 then redirect back to shop
    cart_items = Cartitem.objects.filter(user=current_user)
    print(cart_items)
    cart_count = cart_items.count()
    # if cart_count <= 0:
    #     return redirect('store')
    total = 0
    grand_total = 0
    tax = 0
    quantity = 0
    for i in cart_items:
        total += (i.product.price*i.quantity)
        quantity += i.quantity
    tax = (2 * total)/100
    grand_total = total + tax    
    
    if request.method == 'POST':
        form = Orderform(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_first = form.cleaned_data['address_first']
            data.address_second = form.cleaned_data['address_second']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()


            #generate order number
            day = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))   
            year = int(datetime.date.today().strftime('%Y'))
            d = datetime.date(year,month,day)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            print(order)  
            context = {
                "total" : total,
                "quantity" : quantity,
                "cart_items" : cart_items,
                "tax" : tax,
                "grand_total" : grand_total,
                "form":form,
                "order":order,
            }    
            return render(request,'cart_and_orders/payments.html',context)
        else:
            return redirect('home')
    else:
        form = Orderform()
          
    print(order)    
    context = {
        "total" : total,
        "quantity" : quantity,
        "cart_items" : cart_items,
        "tax" : tax,
        "grand_total" : grand_total,
        "form":form,
        "order":order,
    }        
    return render(request,'cart_and_orders/checkout.html',context)    


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    print(body)

    # store payment details into payment model:
    payment = Payment(
        user = request.user,
        payment_id = body['orderID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    messages.success(request,"Payment was success")
    return render(request,'cart_and_orders/payments.html')
        