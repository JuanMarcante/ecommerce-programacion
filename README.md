Instalaciones requeridas:
Django 3.1

Paquetes extras con pip install:
django-admin-honeypot
django-session-timeout: permite agregar una marca de tiempo a las sesiones para que caduquen de forma independiente, se setean en segundo y para nuestro proyecto es de 3600 segundos (1 hora), pasado ese tiempo sin que el usuario haya estado activo, la sesión se cierra.
python-decouple: ayuda a organizar la configuración para que se pueda cambiar los parámetros sin tener que volver a implementar la aplicación. De este paquete utilizamos la función config en el archivo settings.py