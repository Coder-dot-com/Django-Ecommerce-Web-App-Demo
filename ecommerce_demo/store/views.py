from unicodedata import category
from django.shortcuts import redirect, render

from .forms import ReviewForm

from .models import Product, ProductGallery, ReviewRating
from django.contrib import messages

# Create your views here.

def shop(request):
    return render(request, 'shop.html')


def shop_category(request, category_slug):
    return 

def product_detail(request, category_slug, product_slug):

    product = Product.objects.get(slug=product_slug)

    product_gallery = ProductGallery.objects.filter(product=product)


    reviews = ReviewRating.objects.filter(product=product, visible=True)

    related_products = Product.objects.filter(category=product.category)

    context = {
        'product': product,
        'product_gallery': product_gallery,
        'reviews': reviews,
        'related_products': related_products,
    }


    return render(request, 'product_details.html', context=context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')

    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        try:
            
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.name = form.cleaned_data["name"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.email = form.cleaned_data["email"]
                data.product = product

                data.save()

                print("review submitted successfully")
                messages.success(request, "Thank you! Your review has been saved")


            return redirect(url) 
        
        except Exception as e:
            print("Exception",  e)
            return redirect(url)