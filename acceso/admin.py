from django.contrib import admin
from .models import Alumno, Apoderado, RegistroAcceso

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'curso')
    search_fields = ('nombre', 'rut', 'curso')

@admin.register(Apoderado)
class ApoderadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'telefono', 'autorizado')
    list_filter = ('autorizado',)
    search_fields = ('nombre', 'rut')

@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    # Columnas a mostrar en la tabla
    list_display = ('fecha_hora', 'get_apoderado_nombre', 'get_apoderado_rut', 'permitido')
    # Filtros laterales por fecha y estado de ingreso
    list_filter = ('permitido', 'fecha_hora')
    # Buscador por nombre o RUT del apoderado
    search_fields = ('apoderado__nombre', 'apoderado__rut')
    # Ordenar por el más reciente
    ordering = ('-fecha_hora',)

    @admin.display(description='Apoderado')
    def get_apoderado_nombre(self, obj):
        return obj.apoderado.nombre

    @admin.display(description='RUT')
    def get_apoderado_rut(self, obj):
        return obj.apoderado.rut