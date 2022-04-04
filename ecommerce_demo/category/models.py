from audioop import reverse
from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=1000, blank=True)


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.category_name

    def get_url(self):
        
        return reverse('shop_category', args=[self.slug])
      