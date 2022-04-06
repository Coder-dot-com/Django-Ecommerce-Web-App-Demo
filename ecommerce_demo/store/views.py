from django.shortcuts import get_object_or_404, redirect, render

from category.models import Category

from .forms import ReviewForm

from .models import Product, ProductGallery, ReviewRating
from django.contrib import messages

from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.

def shop(request):

    products = Product.objects.all().filter(is_available=True).order_by('id')
    paginator = Paginator(products, 15)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    
    return render(request, 'shop.html', context=context)



    return render(request, 'shop.html')


def shop_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_available=True).order_by('id')
    paginator = Paginator(products, 15)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    
    product_count = products.count()


    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'shop.html', context=context)









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



def search(request):
    products = None
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_date').filter(Q(description__icontains=keyword) | 
            Q(category__category_name__icontains=keyword) |
             Q(product_name__icontains=keyword)).filter(is_available=True)

            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }




    return render(request, 'shop.html', context)