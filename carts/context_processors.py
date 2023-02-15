from .models import Cart, CartItem
from .views import _cart_id

#Función para que el carrito de la parte superior derecha nos indique la cantidad de artículos que hay en el carrito
def counter(request):
    cart_count = 0

    try:
        cart = Cart.objects.filter(cart_id = _cart_id(request))
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user)
        else:
            cart_items = CartItem.objects.all().filter(cart = cart[:1])
        
        #Para cada artículo contamos la cantidad que el usuario tiene seleccionada
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    
    return dict(cart_count = cart_count)

