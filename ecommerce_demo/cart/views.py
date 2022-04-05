from django.shortcuts import redirect, render
from cart.models import Cart, CartItem, ShippingOption

from store.models import Product

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart_page(request):

    try:
        
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Exception as e:
        return redirect('shop')

    cart_items = CartItem.objects.filter(cart=cart)

    shipping_options = ShippingOption.objects.all()
    
    
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'shipping_options': shipping_options,
    }

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



def clear_cart(request):
    try:
        
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart).delete()
    except Exception as e:
        print(e)
    
    
    return redirect('cart')


def remove_cart_item(request, cart_item_id):
    url = request.META.get('HTTP_REFERER')

    try:
     
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, id=cart_item_id).delete()
    
    except Exception as e:
        print(e)
   
    
    return redirect(url)

def increase_cart_item(request, cart_item_id):
    try:
     
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
        cart_item.quantity += 1
        cart_item.save()
    
    except Exception as e:
        print(e)
   
    
    return redirect('cart')


def decrease_cart_item(request, cart_item_id):
    try:
     
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.delete() 
        else:
            cart_item.save()
    
    except Exception as e:
        print(e)
   
    
    return redirect('cart')