from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
#Con Q hacemos consultas a una base de datos
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct 

# Create your views here.

#Funcion para buscar por categoría slug
def store(request, category_slug=None):
    
    #Condicionamos la consulta a productos en función de si hay un filtro de categoría
    categories = None
    products = None

    if category_slug != None:
        #Investigar esta función
        categories = get_object_or_404(Category, slug = category_slug) 
        products = Product.objects.filter(category = categories, is_available=True).order_by('id')
        #Hacemos la paginación con 6 productos por página
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        #Hacemos la paginación con 6 productos por página
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


#Función para buscar por producto slug
#Tenemos que primero buscar por categoría slig y después por producto slug
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        #Con este línea podemos conocer si el elemento se encuentra ya en el carrito de compras o no
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    #Con esta condición. un usuario no logueado puede ver los artículos de la tienda y evitamos un error del tipo Anonymususer is not iterable
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user = request.user, product_id = single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    #Con esta consulta obtenemos los comentarios de otros usuarios
    reviews = ReviewRating.objects.filter(product_id = single_product.id, status = True)

    #Mostramos los productos de la galería
    product_gallery = ProductGallery.objects.filter(product_id = single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }

    return render(request, 'store/product_detail.html', context)

#Función de búsqueda de productos
def search(request):
    #Queremos saber si desde la URL estmos recibiendo la keyword
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            #Con order_by('-created_date') ordenamos de manera descentente
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    
    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

#Función para las reviews de los usuarios
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            #Actualizamos un comentario en caso de que exista, buscando el review por id
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id)
            form = ReviewForm(request.POST, instance = reviews)
            form.save()
            messages.success(request, 'Gracias, tu comentario ha sido actualizado.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            #Creamos un nuevo comentario
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Gracias, tu comentario fue envido con éxito.')
                return redirect(url)

