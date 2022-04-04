from django.db import models
from category.models import Category
from tinymce.models import HTMLField

import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

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



class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    alt_text = models.CharField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to='store/products', max_length=455)


    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'product gallery'
        verbose_name_plural = 'product gallery'



    def save(self, *args, **kwargs):
        
        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(ProductGallery, self).save(*args, **kwargs)

    def make_thumbnail(self):
        size = 1200

        image = Image.open(self.image)
        width, height = image.size
        width = width*size/height
        image.thumbnail((width,size), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()
        thumb_name = thumb_name.split("/")[-1]

        thumb_filename = thumb_name + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        self.image.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


