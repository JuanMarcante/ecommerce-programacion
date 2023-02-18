"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#Importamos las vistas
from . import views
#Importación para url de archivos estáticos
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    #Para evitar que un ataque de algún hacker, modificamos el admin/ por securelogin/
    path('securelogin/', admin.site.urls),
    #Instalamos el módulo django-admin-honeypot para proporcionarle a posibles hackers una url del admin falsa
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    #Una url vacía lleva automáticamente al home
    path('', views.home, name='home'),
    #Las url de las aplicaciones son las sioguientes
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    #A continuación se incluyen las url para los archivos estáticos
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
