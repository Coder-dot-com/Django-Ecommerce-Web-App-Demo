from django.shortcuts import render

from .models import Product, ProductGallery

# Create your views here.

def shop(request):
    return render(request, 'shop.html')


def shop_category(request, category_slug):
    return 

def product_detail(request, category_slug, product_slug):

    product = Product.objects.get(slug=product_slug)

    product_gallery = ProductGallery.objects.filter(product=product)


    context = {
        'product': product,
        'product_gallery': product_gallery,
    }


    return render(request, 'product_details.html', context=context)

def submit_review(request, product_id):
    pass