from django.db import models
from store.models import Product

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, unique=True)
    time_created = models.DateTimeField(auto_now_add=True)


    def calculate_cart_total(self):
        print("calculate cart_total function")
        total = 0
        try:
            cart_items = CartItem.objects.filter(cart=self)
            for cart_item in cart_items:
                total += (cart_item.price * cart_item.quantity)
       
        except Exception as e:
            print(e)

        return total

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    time_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    sub_total = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField()

   

    def calculate_sub_total(self):
        self.sub_total = self.price * self.quantity
        self.save()



    def __str__(self):
        return f"{self.product.product_name} - {self.cart.cart_id}"


