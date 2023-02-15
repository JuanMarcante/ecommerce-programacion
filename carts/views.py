from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
#Con esta librería controlamos el acceso al sitio si el usuario esta logueado o no
from django.contrib.auth.decorators import login_required

# Create your views here.

#Función privada para vincular el carrito a la sesión del usuario
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        #Se crea una nueva sesión si es que no existe
        cart = request.session.create()
    
    return cart

#Función para agregar a carrito
def add_cart(request, product_id):
    #Seleccionamos el producto a agregar por el id
    product = Product.objects.get(id=product_id)

    current_user = request.user
    if current_user.is_authenticated:
        #Lógica del carrito cuando el usuario esta autenticado
        product_variation = []

        if request.method == 'POST':#Si el método es POST, aplicamos un bucle para contar la cantidad de variaciones
            for item in request.POST:
                key = item #Capturamos el nombre o tipo de variación
                value = request.POST[key] #Capturamos el valor
                #Verificamos si la variacion existe en la base de datos
                try:
                    #Buscamos por producto y variación
                    variation = Variation.objects.get(product=product, variation_category__iexact = key, variation_value__iexact = value)
                    product_variation.append(variation)
                except:
                    pass

        #Cargamos el carrito según el usuario ya haya elegido productos con variaciones iguales o no
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity +=1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user = current_user)
                #Insertamos las variaciones al carrito de compras sólo si no están en blanco
                if len(product_variation) > 0:
                    item.variations.clear()#Limpiamos por las dudas que ya tenga valores
                    item.variations.add(*product_variation)
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            #Insertamos las variaciones al carrito de compras sólo si no están en blanco
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()
        return redirect('cart')


    else:
        #Hacemos la cantidad de variaciones como talla o color sean dinámicas
        product_variation = []

        if request.method == 'POST':#Si el método es POST, aplicamos un bucle para contar la cantidad de variaciones
            for item in request.POST:
                key = item #Capturamos el nombre o tipo de variación
                value = request.POST[key] #Capturamos el valor
                #Verificamos si la variacion existe en la base de datos
                try:
                    #Buscamos por producto y variación
                    variation = Variation.objects.get(product=product, variation_category__iexact = key, variation_value__iexact = value)
                    product_variation.append(variation)
                except:
                    pass


        #Verificamos si el carrito existe o no con try para evitar que se trabe la aplicación
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            ) 
        cart.save()

        #Cargamos el carrito según el usuario ya haya elegido productos con variaciones iguales o no
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity +=1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                #Insertamos las variaciones al carrito de compras sólo si no están en blanco
                if len(product_variation) > 0:
                    item.variations.clear()#Limpiamos por las dudas que ya tenga valores
                    item.variations.add(*product_variation)
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            #Insertamos las variaciones al carrito de compras sólo si no están en blanco
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

            cart_item.save()
        return redirect('cart')

#Función para eliminar de carrito
def remove_cart(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user = request.user, id = cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if(cart_item.quantity) > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id = product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user = request.user, id = cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()
    return redirect('cart')

#Renderizamos store.html
def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        #Con este for sabemos la cantidad de cada tipo de productos que hay en el carrito y el precio
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (21 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quentity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        #Con este for sabemos la cantidad de cada tipo de productos que hay en el carrito y el precio
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (21 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/checkout.html', context)
