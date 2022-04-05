from django.shortcuts import redirect, render

from cart.models import Cart, CartItem, ShippingOption
from cart.views import _cart_id

# Create your views here.


def checkout(request):
    cart = Cart.objects.get(cart_id=_cart_id(request))
     



    #if post need to update the shipping option
    if request.POST:
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
