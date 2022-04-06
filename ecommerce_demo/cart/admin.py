from django.contrib import admin

from cart.models import Cart, CartItem, ShippingOption

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ShippingOption)