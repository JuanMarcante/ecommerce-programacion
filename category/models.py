from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255, blank=True)
    #slug representa un valor al final de la url que representa a la entidad. Se usa en app de Ecommerce
    slug = models.CharField(max_length=100, unique=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        #Con esto evitamos que Django pluralice los sustantivos, lo cual lleva a errores de ortografía
        #Django por defecto pone mayúsculas iniciales
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    #Función para hacer urls dinámicas según slug de categoría
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name