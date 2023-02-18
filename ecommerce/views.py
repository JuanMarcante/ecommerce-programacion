from django.shortcuts import render
from store.models import Product, ReviewRating

def home(request):
    #Consulta para traer todos los productos según condición de activos
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    #Para cada uno de los productos traemos las calificaciones que ha recibido
    for product in products:
        reviews = ReviewRating.objects.filter(product_id = product.id, status = True)

    #Enviamos al context de la función los productos y sus calificaciones
    context = {
        'products': products,
        'reviews': reviews,
    }
    #Renderizamos el archivo html
    return render(request, 'home.html', context)