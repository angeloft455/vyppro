from django.contrib import admin
from .models import Servicio, Formulario, Galeria

# Register your models here.
class FormularioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'empresa', 'servicio', 'mensaje_corto', 'estado', 'fecha')
    
    list_editable = ('estado',) 
    
    list_filter = ('estado', 'servicio')

    readonly_fields = ('nombre', 'apellido', 'empresa', 'telefono', 'correo', 'servicio', 'mensaje', 'fecha')

    def mensaje_corto(self, obj):
        return obj.mensaje[:50] + '...' if len(obj.mensaje) > 50 else obj.mensaje
    mensaje_corto.short_description = 'Mensaje'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

class GaleriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'imagen', 'fecha', 'servicio')
    
    list_filter = ('servicio',)

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'visible')
    list_editable = ('visible',)
    list_filter = ('visible',)

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Formulario, FormularioAdmin)
admin.site.register(Galeria, GaleriaAdmin)

