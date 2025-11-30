from django.contrib import admin
from .models import (
    Paciente, 
    Dentista, 
    FichaClinica, 
    Tratamiento, 
    Evolucion, 
    Cita, 
    TarifaInsumo
)

# Configuración para ver tratamientos dentro de la ficha
class TratamientoInline(admin.TabularInline):
    model = Tratamiento
    extra = 1

# Configuración para ver evoluciones dentro de la ficha
class EvolucionInline(admin.TabularInline):
    model = Evolucion
    extra = 1
    # Hacemos que las evoluciones pasadas sean solo lectura en el inline
    def get_readonly_fields(self, request, obj=None):
        if obj: # Si la ficha ya existe
            return [f.name for f in self.model._meta.fields]
        return []

@admin.register(FichaClinica)
class FichaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_creacion')
    inlines = [TratamientoInline, EvolucionInline]

@admin.register(Evolucion)
class EvolucionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'dentista', 'ficha')
    # BLOQUEO DE EDICIÓN: Si ya existe, es solo lectura
    def get_readonly_fields(self, request, obj=None):
        if obj: 
            return ('ficha', 'dentista', 'nota_clinica')
        return ()

# Registro simple del resto de modelos
admin.site.register(Paciente)
admin.site.register(Dentista)
admin.site.register(Tratamiento)
admin.site.register(Cita)
admin.site.register(TarifaInsumo)