from django.db import models
from django.contrib.auth.models import User
from suscripciones.models import Plan




# Create your models here.

class Pago(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    TIPO_PAGO_CHOICES = [
        ('EF', 'Efectivo'),
        ('TR', 'Transferencia'),
    ]
    tipo_pago = models.CharField(max_length=2, choices=TIPO_PAGO_CHOICES)

    def __str__(self):
        return f'Pago de {self.user.username}'


class Asistencia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    numero_clase = models.IntegerField()

    def __str__(self):
        return f"{self.usuario.username} - Clase {self.numero_clase}"