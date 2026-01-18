from .models import Servicio

def menu_servicios(request):
    servicios_visibles = Servicio.objects.filter(visible=True)
    
    return {
        'servicios_menu': servicios_visibles
    }