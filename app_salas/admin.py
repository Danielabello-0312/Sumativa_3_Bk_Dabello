from django.contrib import admin
from .models import Sala, Reserva

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'capacidad_maxima', 'disponible']
    list_filter = ['disponible']
    search_fields = ['nombre']

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['rut', 'sala', 'inicio', 'termino']
    list_filter = ['sala', 'inicio']
    search_fields = ['rut', 'sala__nombre']