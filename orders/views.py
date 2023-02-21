from django.shortcuts import render, redirect
from django.http import JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from django.http import HttpResponse
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
#Función para crear los pagos
def payments(request):
    #Almacenamos en una variable los datos del pago
    body = json.loads(request.body)
    #Buscamos la órden a la cual corresponde el pago
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = body['orderID'])

    #Instanciamos el pago con sus datos
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_id = order.order_total,
        status = body['status'],
    )
    #Guardamos el pago
    payment.save()

    #Asociamos el pago a la órden, cambiamos el estado de la órden y guardamos
    order.payment = payment
    order.is_ordered = True
    order.save()

    #Mover todos los items de carritos hacia la tabla de order product
    cart_items = CartItem.objects.filter(user = request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    #Eliminamos en carrito una vez que el cliente ha hecho la compra
    CartItem.objects.filter(user=request.user).delete()

    #Envío de correo electrónico cuando el cliente efectúa una compra
    mail_subject = 'Gracias por tu compra.'
    body = render_to_string('orders/order_recieved_email.html', {
        'user' : request.user,
        'order' : order,
    })

    to_email = request.user.email
    send_email = EmailMessage(mail_subject, body, to=[to_email])
    send_email.send()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)

#Función para realizar el pedido
def place_order(request, total = 0, quantity = 0):
    #Tomamos los datos del usuario y su carrito
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    #Retornamos a store si no hay carrito
    if cart_count <= 0:
        return redirect('store')
    
    #Ponemos en cero el total y el impuesto
    grand_total = 0
    tax = 0

    #Calculamos el total y la cantidad para los artículos dentro del carrito
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    #Cáclulo de impuesto IVA 21% y el total a pagar
    tax = (21 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        #Si el formulario es válido
        if form.is_valid():
            data = Order()
            data.user = current_user
            #Capturamos sus datos
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            #Traemos los valores calculados más arriba
            data.order_total = grand_total
            data.tax = tax
            #Traemos la dirección IP del usuario 
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #Generamos el numero de orden en función de la fecha actual
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered = False, order_number = order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax':tax,
                'grand_total': grand_total,
            }

            return render(request, 'orders/payments.html', context)
        return redirect('checkout')
    else:
        return redirect('checkout')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number = order_number, is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id = order_id)

        subtotal = 0

        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id = transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)

    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
