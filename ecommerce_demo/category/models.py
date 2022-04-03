from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    seo_keywords = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(max_length=1000, blank=True)

    category_position = models.IntegerField(null=True, blank=True, default=999)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.category_name