from django.shortcuts import redirect, render

from cart.models import Cart, CartItem, ShippingOption
from cart.views import _cart_id
from order.forms import OrderForm
from order.models import Order
import datetime

# Create your views here.


def checkout(request):
    cart = Cart.objects.get(cart_id=_cart_id(request))
     



    #if post need to update the shipping option
    if request.method == 'POST':
        print(request.POST)
        shipping_option = request.POST['shipping'].split("_")[0]
        cart.shipping_option = ShippingOption.objects.get(option=shipping_option)
        cart.save()

        #set the cart shipping foreign key to the selected one
        



    if not cart.shipping_option:
        return redirect('cart')  


    cart_items = CartItem.objects.filter(cart=cart)  

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }

    return render(request, 'checkout.html', context=context)


def payment(request):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart)  

    if request.method == 'POST':
        print(request.POST)
        #Here create the order object using the form cleaned data
        form = OrderForm(request.POST)
        if form.is_valid():
            
            data = Order()
            data.cart_id = cart
            data.billing_first_name = form.cleaned_data['billing_first_name']
            data.billing_last_name = form.cleaned_data['billing_last_name']
            data.billing_phone = form.cleaned_data['billing_phone']
            data.billing_email = form.cleaned_data['billing_email']
            data.billing_address_line_1 = form.cleaned_data['billing_address_line_1']
            data.billing_address_line_2 = form.cleaned_data['billing_address_line_2']
            data.billing_country = form.cleaned_data['billing_country']
            data.billing_state = form.cleaned_data['billing_state']
            data.billing_postcode = form.cleaned_data['billing_postcode']
            data.billing_city = form.cleaned_data['billing_city']



            if 'different_shipping_address' in request.POST:
                data.ship_diff_to_bill = True
            else:
                data.ship_diff_to_bill = False
             
            data.ship_first_name = form.cleaned_data['ship_first_name']
            data.ship_last_name = form.cleaned_data['ship_last_name']
            data.ship_phone = form.cleaned_data['ship_phone']
            data.ship_email = form.cleaned_data['ship_email']
            data.ship_address_line_1 = form.cleaned_data['ship_address_line_1']
            data.ship_address_line_2 = form.cleaned_data['ship_address_line_2']
            data.ship_country = form.cleaned_data['ship_country']
            data.ship_state = form.cleaned_data['ship_state']
            data.ship_postcode = form.cleaned_data['ship_postcode']
            data.ship_city = form.cleaned_data['ship_city']
            data.shipping_method = cart.shipping_option.option
            
            data.shipping_price =  cart.shipping_option.price

            data.payment_method = "stripe"

            
            data.order_total = cart.calculate_cart_total_with_shipping()



            data.save()
        
            #Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")

            order_number = current_date + str(data.id)
            data.order_number = order_number

            data.save()




    #Try to get the order object so if user gets the page it makes sure order exists
    try:
        order = Order.objects.filter(cart_id=cart).latest('created_at')
    except Exception as e:
        print(e)
        return redirect('checkout')
    

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'order': order,
    }

    return render(request, 'payment.html', context=context)
