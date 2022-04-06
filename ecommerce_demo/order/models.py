from django.db import models
from cart.models import Cart
from store.models import Product

# Create your models here.

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('On hold', 'On hold'),
    )

    cart_id = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=200, unique=True)
    billing_first_name = models.CharField(max_length=50)
    billing_last_name = models.CharField(max_length=50)
    billing_phone = models.CharField(max_length=15, blank=True, null=True)
    billing_email = models.EmailField(max_length=100)
    billing_address_line_1 = models.CharField(max_length=15)
    billing_address_line_2 = models.CharField(max_length=50, blank=True)
    billing_country = models.CharField(max_length=50)
    billing_state = models.CharField(max_length=50)
    billing_city = models.CharField(max_length=50)
    billing_postcode = models.CharField(max_length=50)
    shipping_method = models.CharField(max_length=200, null=True)
    shipping_price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    payment_method = models.CharField(max_length=100, blank=True)
    order_total = models.DecimalField(max_digits=7, decimal_places=2)

    status = models.CharField(max_length=10, choices=STATUS)
    
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ship_diff_to_bill = models.BooleanField(default=False)
    ship_first_name = models.CharField(max_length=50, blank=True)
    ship_last_name = models.CharField(max_length=50, blank=True)
    ship_phone = models.CharField(max_length=15, blank=True)
    ship_email = models.EmailField(max_length=100, blank=True)
    ship_address_line_1 = models.CharField(max_length=15, blank=True)
    ship_address_line_2 = models.CharField(max_length=50, blank=True)
    ship_country = models.CharField(max_length=50, blank=True)
    ship_state = models.CharField(max_length=50, blank=True)
    ship_city = models.CharField(max_length=50, blank=True)
    ship_postcode = models.CharField(max_length=50, blank=True)
    payment_intent_id = models.CharField(max_length=300)    


    def __str__(self):
        return self.order_number



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    sub_total = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.product.product_name


class Payment(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    payment_intent_id = models.CharField(max_length=300)    
    payment_method = models.CharField(max_length=300)
    amount_paid = models.CharField(max_length=300)
    status = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.CharField(max_length=5000, blank=True)

    def __str__(self):
        return self.payment_intent_id