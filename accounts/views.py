from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserProfileForm, UserForm
from .models import Account, UserProfile
from orders.models import Order
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from carts.views import _cart_id
from carts.models import Cart, CartItem
#Con la librería requests podemos capturar parámetros de una url en la cual estamos
import requests

# Create your views here.
#La función register permite el registro de nuevos usuarios
def register(request):
    #Elegimos el formulario RegistrationForm el cual debe ser importado
    form = RegistrationForm()
    #El métos que mos debe pasar el formulario desde el template es post
    if request.method == 'POST':
        #El formulario toma los datos enviados desde el template
        form = RegistrationForm(request.POST)
        #validamos los datos
        if form.is_valid():
            #Guardamos los datos enviados en el formulario en variables
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #Genermos el username a partir del correo electrónico. No existe en la base de datos en la realidad
            username = email.split('@')[0]
            #Registramos al usuario nuevo con los datos pasados a través del formulario
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            #Guardamos el usuario creado en la base de datos
            user.save()

            #Creación del UserProfile en la tabla
            profile = UserProfile()
            profile.user_id = user.id
            #El perfil se crea automáticamente con una foto estándar, luego puede ser modificada
            profile.profile_picture = 'default/default-user.png'
            #Guardamos el perfil en la base de datos
            profile.save() 

            #Activación de usuario con envío de mail
            #Definimos la url donde el usuario debe darle click cuando le llegue el mail
            current_site = get_current_site(request)
            #Asunto del email
            mail_subject = 'Por favor, active su cuenta.'
            #Cuerpo del mail
            body = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                #Ciframos la clave primaria por seguridad
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #Token
                'token': default_token_generator.make_token(user),

            })
            #Envío de correo electrónico
            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()


            messages.success(request, 'Se registró el usuario exitosamente.')
            return redirect('/accounts/login/?command=verification&email='+email)

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

#Función para login 
def login(request):
    #Desde el template se envía el método post
    if request.method == 'POST':
        #Guardamos los datos de login en variables
        email = request.POST['email']
        password = request.POST['password']

        #Autenticamos y verificamos que coincidan
        user = auth.authenticate(email=email, password=password)

        if user is not None:

            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    #Con este bucle for recolectamos todas las elecciones que haga el usuario cuanto no está en sesión
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    #Con este bucle for recolectamos todas las elecciones que haga el usuario cuanto si está en sesión
                    cart_item = CartItem.objects.filter(user = user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    #Ahora que tenemos estas dos listas product_variation y ex_var_list
                    #las evaluamos y trabajamos con aquellas que tengan valores coincidentes
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        #En caso de que los artículos que no coincidan, actualizamos cart_item y le asignamos el usuario al item
                        else:
                            cart_item = CartItem.objects.get(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            auth.login(request, user)
            messages.success(request, 'Has iniciado sesión.')
            #Cuando el usuario arma un carrito sin haber iniciado sesión y luego le da a pagar, queremos que el sitio
            #lo redireccione automáticamente a checkout y no al dashboard del usuario
            url = request.META.get('HTTP_REFERER')
            #Capturamos el parámetro
            try:
                #Usamos la librería requests para capturar todos los parámetros
                query = requests.utils.urlparse(url).query
                #Nos quedamos con los parámetros a la derecha del '?' en la url next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                #por defecto si no encuentra el parse, redirige al dashboard
                return redirect('dashboard')
        else:
            messages.error(request, 'Email o contraseña inválidos. Ingréselos correctamente.')
            return redirect('login')

    return render(request, 'accounts/login.html')

#Esta función permite salir de sesión y el login es requerido
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Sesión Finalizada')

    return redirect('login')


#Función para activar cuenta a través de email
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    #Si los datos son válidos
    if user is not None and default_token_generator.check_token(user, token):
        #Modificamos el estado del usuario y guardamos en la base de datos
        user.is_active = True
        user.save()
        messages.success(request, 'Tu cuenta ha sido activada')
        return redirect('login')
    #En caso de que los datos no sean válidos, redirigimos al register
    else:
        messages.error(request, 'La activación no fue realizada')
        return redirect('register')

#Con esta función el usuario puede visualizar su dashboard o tablero personal
@login_required(login_url='login')
def dashboard(request):
    #Creamos el objeto orders ordenado según fecha y filtramos según el id del usuario y según hayan sido ordenados o no
    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id, is_ordered = True)
    #Calculamos la cantidad de órdenes realizadas por el usuario
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id = request.user.id)
    context ={
        'orders_count': orders_count,
        'userprofile': userprofile,
    }

    return render(request, 'accounts/dashboard.html', context)

#Con esta función el usuario puede recuperar su contraseña
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #Creación y envío del mail
            current_site = get_current_site(request)
            mail_subject = 'Restablecer Contraseña'
            body = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            messages.success(request, 'Un mail fue enviado a tu bandeja de entrada.')
            return redirect('login')
        else:
            messages.error(request, 'La cuenta de usuario no existe')
            return redirect(forgotPassword)

    return render(request, 'accounts/forgotPassword.html')

#Función para validar el cambio de contraseña
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Por favor, restablecé tu contraseña')
        return redirect('resetPassword')
    else:
        messages.error(request, 'El link ha expirado')
        return redirect('login')

#Función para restablecer la contraseña
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        #Si las contraseñas coinciden se produce el cambio de la misma y se guardan las modificaciones en las base de datos
        if password == confirm_password:
            uid == request.session.get('uid')
            user = Account.objects.filter(pk=uid)
            user.set_password(password)
            user.save()
            #Aviso de cambio de contraseña exitoso
            messages.success(request, 'La contraseña se restableción correctamente.')
            #Redirigimos al login
            return redirect('login')
        else:
            #Aviso de error
            messages.error(request, 'La contraseña no concuerda.')
            #Redirigimos a resetPassword
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

#Función para conocer las órdenes de cada usuario
def my_orders(request):
    #Buscamos las órdenes desde la base de datos y filtramos por usuario y si fueron ordenadas (pedidas). Se ordenan según fecha empezando por la última
    orders = Order.objects.filter(user = request.user, is_ordered=True).order_by('created_at')
    context = {
        'orders': orders,
    }
    
    #Devolvemos todas las órdenes del usuario a través del template my_orders.html
    return render(request, 'accounts/my_orders.html', context)

#Funcion para editar el perfil. Se requiere de un login
@login_required(login_url='login')
def edit_profile(request):
    #Tomamos el perfil del usuario
    userprofile = get_object_or_404(UserProfile, user = request.user)
    if request.method == 'POST':
        #Tomamos los formularios de usuario y perfil
        user_form = UserForm(request.POST, instance = request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance = userprofile)
        #Si los datos son válidos se guardan los datos en la base de datos, se avisa de que fue exitoso y se redirige a edit_profile
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Su información fue guardada con éxito')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
        }
    
    return render(request, 'accounts/edit_profile.html', context)

#Función para el cambio de contraseña. Se requiere login
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        #Tomamos los datos enviados por el usuario
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        #Tomamos la cuenta del usuario
        user = Account.objects.get(username__exact = request.user.username)

        #Se procede a validar y si todo está OK se genera la contraseña nueva y se guardan los datos en la base de datos
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()

                messages.success(request, 'La contraseña fue actualizada exitosamente.')
                return redirect('change_password')
            else:
                messages.error(request, 'Por favor, ingrese un password válido.')
                return redirect('change_password')
        else:
            messages.error(request, 'La contraseña nueva y su confirmación no coinciden')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')
                

