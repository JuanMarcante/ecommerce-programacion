from django.contrib import admin
from .models import Product, Variation,ReviewRating, ProductGallery
#Este módulo lo instalamos con pip install django-admin-thumbnails y nos permite previsualizar las imagenes de los productos
import admin_thumbnails

# Register your models here.

#Creamos esta clase para poder ver más de una foto de cada products
@admin_thumbnails.thumbnail('image')
class ProductGalleryInine(admin.TabularInline):
    model = ProductGallery
    extra = 1

#Agregamos propiedades a cómo se visualiza el listado de productos en el Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    #Con esto podemos ver las fotos de la galería
    inlines = [ProductGalleryInine]

#Agregamos propiedades a cómo se visualiza el listado de propiedades o variaciones en el Admin
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category', 'variation_value', 'is_active')



admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
