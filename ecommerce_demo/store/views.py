from django.shortcuts import render

# Create your views here.

def shop(request):
    return render(request, 'shop.html')


def shop_category(request, category_slug):
    return 

def product_detail(request, category_slug, product_slug):
    pass

def submit_review(request, product_id):
    pass