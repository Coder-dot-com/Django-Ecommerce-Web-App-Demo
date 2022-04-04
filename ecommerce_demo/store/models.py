from django.db import models
from category.models import Category
from tinymce.models import HTMLField

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_image_alt = models.CharField(max_length=2000, null=True, blank=True)

    description = HTMLField(max_length=7500, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    main_image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_date =  models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    num_sold = models.IntegerField(default=0)
