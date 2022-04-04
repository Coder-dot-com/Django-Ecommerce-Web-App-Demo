from django.shortcuts import get_object_or_404, render
from category.models import Category

from store.models import Pages, Product

def home(request):

    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'home.html', context=context)


def contact_us(request):
    return render(request, 'contact-us.html')

def page(request, page=None):
    page = get_object_or_404(Pages, page_title=str(page))

    context = {
        'page': page,
    }

    return render(request, 'generic-page.html', context=context)



 