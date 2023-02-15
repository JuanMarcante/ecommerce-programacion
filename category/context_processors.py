from .models import Category

def menu_links(request):
    links = Category.objects.all()
    #Retornamos un diccionario con los resultados
    return dict(links=links)
