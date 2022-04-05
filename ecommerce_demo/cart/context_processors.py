from .models import Cart, CartItem
from .views import _cart_id

def slider_cart(request):
    if 'admin' in request.path:
        return ()
    else:
        cart_count = 0
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart)
            for cart_item in cart_items:
                cart_count += cart_item.quantity


        
        except Cart.DoesNotExist:
            cart_items = []
        
        total = cart.calculate_cart_total()
        
        return dict(cart_count=cart_count, draw_cart_items=cart_items, slider_total=total)


