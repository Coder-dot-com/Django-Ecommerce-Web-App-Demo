from django.shortcuts import render

# Create your views here.

def cart_page(request):
    
    
    context = None

    return render(request, 'cart.html', context=context)