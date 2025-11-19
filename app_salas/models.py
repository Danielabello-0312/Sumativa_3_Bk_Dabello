from django.db import models
from django.utils import timezone
from datetime import timedelta

class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad_maxima = models.IntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    rut = models.CharField(max_length=12)
    inicio = models.DateTimeField(default=timezone.now)
    termino = models.DateTimeField(blank=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.termino:
            self.termino = self.inicio + timedelta(hours=2)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rut} - {self.sala.nombre}"