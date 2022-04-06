from ecommerce_demo.celery import app
from order.models import Order, OrderProduct
from decouple import config

from django.core.mail import send_mail
from django.template.loader import render_to_string


@app.task
def order_placed_email(order_number):
    

    order = Order.objects.get(order_number=order_number)
    print(order.id)

    if not order.order_conf_email_sent:

        order_items = OrderProduct.objects.all().filter(order=order)
        print(f"order_items: {order_items}") 



        context_for_order_placed = {
            'order': order,
            'order_items': order_items,
        }

        message = render_to_string('emails/order_placed_email.html', context=context_for_order_placed)

        site_email = config['SITE_EMAIL']

        send_mail(
            subject=f'Thank you for your order',  
            message=message, 
            from_email=f'{site_email}', 
            recipient_list=[order.billing_email], 
            fail_silently=False,
            html_message=message,
        )

        order.order_conf_email_sent = True
        order.save()
    else:
        print("Order conf Email already sent")