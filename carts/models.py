from django.db import models
from store.models import Product, Variation
from accounts.models import Account

# Create your models here.
#Clase para el carrito de compra
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


#Elemento o producto que se elige y agrega al carrito
class CartItem(models.Model):
    #Establecemos las relaciones con las tablas de usuario y producto
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #Almacenamos las variaciones como color y talle en el carrito de compras
    variations = models.ManyToManyField(Variation, blank=True)

    #Establecemos las relaciones con la tabla carrito
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    #Devolvemos un subtotal sin impuestos (tax)
    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product