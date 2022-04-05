from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order        
        fields = ['billing_first_name',
        'billing_last_name',
        'billing_phone',
        'billing_email',
        'billing_address_line_1',
        'billing_address_line_2',
        'billing_country',
        'billing_state',
        'billing_city',
        'billing_postcode',
        'ship_first_name',
        'ship_last_name',
        'ship_phone',
        'ship_email',
        'ship_address_line_1',
        'ship_address_line_2',
        'ship_country',
        'ship_state',
        'ship_city',
        'ship_postcode',
        'payment_method',]