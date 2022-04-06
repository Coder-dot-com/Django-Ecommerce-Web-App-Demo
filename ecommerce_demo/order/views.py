from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from cart.models import Cart, CartItem, ShippingOption
from cart.views import _cart_id
from ecommerce_demo.emails.tasks import order_placed_email
from ecommerce_demo.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, STRIPE_ENDPOINT_SECRET
from order.forms import OrderForm
from order.models import Order, OrderProduct, Payment
import datetime
import stripe

from django.views.decorators.csrf import csrf_exempt


#Initialize stripe
stripe.api_key = STRIPE_SECRET_KEY


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


    # Creating Stripe payment intent
    grand_total = order.order_total

    intent = stripe.PaymentIntent.create(
        amount = int(grand_total*100),
        currency = "USD",
        payment_method_types = [
            "card",
            ],
        )
    
    payment_intent_id = intent.id
    order.payment_intent_id = payment_intent_id
    order.save()
    
    return_url = request.build_absolute_uri(reverse('success',kwargs={}))


    context = {
        'order': order,
        'cart_items': cart_items,
        'total': grand_total,
        'grand_total': grand_total,
        'payment_method': data.payment_method,
        'client_secret': intent.client_secret,
        'stripe_pub_key': STRIPE_PUBLIC_KEY,
        'return_url': return_url,
        
    }




    





    return render(request, 'payment.html', context=context)


def _post_payment_success(request, payment_intent):
    print("CREATING ORDER ITEMS")
    payment_intent = str(payment_intent)

    order = Order.objects.get(payment_intent_id=payment_intent)
    order_items = OrderProduct.objects.filter(order=order)


    if not order_items:

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))

            cart_items = CartItem.objects.filter(cart=cart)


            # loop through cart items and move to order item
            order.is_ordered = True
            order.save()
            print(f"cart items are {cart_items}")

            for item in cart_items:
                print(item)
                orderproduct = OrderProduct.objects.create(
                    order = order,
                    cart_id = cart,
                    product = item.product,        
                    quantity = item.quantity,
                    price = item.price,
                    sub_total = item.sub_total,
                    )
                        
                # add counter for each product(num sold, and increment)
                item.product.num_sold += item.quantity
                item.product.stock -= item.quantity
                item.product.save()

            # Clear cart
            cart_items = CartItem.objects.filter(cart=cart).delete()
            cart.shipping_option = None
            cart.save()


                #Get the new order items
            order_items = OrderProduct.objects.filter(order=order)



        except Exception as e:
            print("Exception creating order product")
            print(e)
            pass

 

    #Repeat this for webhook incase user browser closes during payment

    
    try:
        order_placed_email.delay(order.order_number) 
        print("email scheduled")
    except Exception as e:
        print(e)

    context = {
        'order': order,
        'order_items': order_items,
    }

    return context





def success(request):
    payment_intent = request.GET['payment_intent']

    context = _post_payment_success(request, payment_intent=payment_intent)       
    
    return render(request, 'success.html', context=context)





#Verify payment succeeded and create payment object
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = STRIPE_SECRET_KEY
    endpoint_secret = STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event '# Move the logic that the redirect url view is dependant on
    # to success view to ensure it's performed in correct order so that page renders properly
    if event['type'] == 'charge.succeeded':
        print("Payment was successful.")
        payment_intent_id = (event['data']['object']['payment_intent'])
        order = Order.objects.get(payment_intent_id=payment_intent_id)
        cart = order.cart_id
        payment = Payment(
            cart_id = cart,
            order = order,
            payment_intent_id = payment_intent_id,
            payment_method = "Stripe",
            amount_paid = (event['data']['object']['amount']/100),
            status = event['type'],
            response = event,

        )
        payment.save()
        order.is_ordered = True
        order.save()

        _post_payment_success(request, payment_intent=payment_intent_id)


    return HttpResponse(status=200)
