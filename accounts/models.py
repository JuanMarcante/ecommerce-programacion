from django.db import models

#Importamos estos módulos extender nuestras clases
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
#Clase para crear un nuevo usuario y un nuevo Super Admin Usuario
class MyAccountManager(BaseUserManager):

    #Función para crear usuario
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('El usuario debe tener un email.')
        
        if not username:
            raise ValueError('El usuario debe tener un username.')

        user = self.model(
            email=self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        #Seteamos la contraseña
        user.set_password(password)

        #Guardamos en la Base de Datos
        user.save(using=self._db)

        return user

    #Función para crear superusuario
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        #Atributos propios de super usuario
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        
        #Guardamos en la Base de Datos
        user.save(using=self._db)

        return user

#Clase para modificar la seguridad por defecto de Django
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    #Campos atributos de Django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    #Ahora modificamos los valores que Django trae por defecto
    USERNAME_FIELD = 'email' 

    #Definimos los campor requeridos u obligatorios
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    #Instanciamos nuestra clase previamente creada
    objects = MyAccountManager()

    #Función para devolver los cometarios de los usuarios en la calificación de los productos
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    #Con esta función hacemos que al listar los usuarios, aparezca un label con su email
    def __str__(self):
        return self.email

    #Con esta función definimos si un usuario tiene permisos de adminsitrados
    def has_perm(self, perm, obj=None):
        return self.is_admin

    #Permiso de acceso a los módulos
    def has_module_perms(self, add_label):
        return True

#Con esta clase creamos el perfil del usuario
class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=100, blank= True)
    address_line_2 = models.CharField(max_length=100, blank= True)
    profile_picture = models.ImageField(upload_to='userprofile', blank = True, null=True)
    city = models.CharField(max_length=20, blank= True)
    state = models.CharField(max_length=20, blank= True)
    country = models.CharField(max_length=20, blank= True)

    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'



