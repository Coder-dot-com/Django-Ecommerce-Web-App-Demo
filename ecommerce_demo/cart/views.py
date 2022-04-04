from django.shortcuts import redirect, render
from cart.models import Cart, CartItem

from store.models import Product

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart_page(request):
    
    
    context = None

    return render(request, 'cart.html', context=context)


def add_cart(request, product_id):

        #Get product

    try:
        product = Product.objects.get(id=product_id)
    except Exception as e:
        return redirect('shop')

        # Get product price

    if product.sale_price:
        price = product.sale_price
    else:
        price = product.price

        
        #Create/Get cart and cartitem
    try:
        
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    
    except Cart.MultipleObjectsReturned:
        Cart.objects.filter(cart_id=_cart_id(request)).delete()
        cart = Cart.objects.create(cart_id=_cart_id(request))

        #Get quantity from the form
    
    print(request.POST)
    quantity = int(request.POST['quantity'])


    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.price = price
        cart_item.save()


    except CartItem.DoesNotExist:
    
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity, price=price)

    #Save the data to a CartItem 
        
    return redirect('cart')