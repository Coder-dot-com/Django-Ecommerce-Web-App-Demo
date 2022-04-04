from django.contrib import admin

from store.models import Product, ProductGallery, ReviewRating

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'sale_price', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]




admin.site.register(Product, ProductAdmin)


admin.site.register(ReviewRating)