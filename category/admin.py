from django.contrib import admin
from .models import Category

# Register your models here.

#Clase para la administración de las categorías
class CategoryAdmin(admin.ModelAdmin):
    #Autocompletado de slug en función de Category name
    prepopulated_fields = {'slug': ('category_name',)}
    #Indicamos los elementos que quermos ver
    list_display = ('category_name', 'slug')


admin.site.register(Category, CategoryAdmin)