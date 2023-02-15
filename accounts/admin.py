from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html

#Modificamos el tablero de usuarios
class AccountAdmin(UserAdmin):
    #Definimos las propiedades que queremos visualizar
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    #Definimos un link para poder ir al detalle del usuario
    list_display_link = ('email', 'first_name', 'last_name')
    #Definimos campos de sólo lectura
    readonly_fields = ('last_login', 'date_joined')
    #Definimos orden ascendente en función de fecha en la que el usuario se unió a la aplicación
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

#Con esta clase administramos la función del perfil del usuario
class UserProfileAdmin(admin.ModelAdmin):
    #Con esta función controlamos las imagenes dentro del django administration
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50%;">'.format(object.profile_picture.url))
    
    thumbnail.short_description = 'Imagen de Perfil'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)