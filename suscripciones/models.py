from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad_clases = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre
    

class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL, null=True)
    codigo_qr = models.ImageField(upload_to='qrcodes', blank=True, null=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    TIPO_PAGO_CHOICES = [
        ('EF', 'Efectivo'),
        ('TR', 'Transferencia'),
    ]
    tipo_pago = models.CharField(max_length=2, choices=TIPO_PAGO_CHOICES)
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        from administracion.models import Asistencia  # Importación local
        if self.fecha_fin:
            # Ajusta la fecha de finalización para que sea un día después
            self.fecha_fin += timedelta(days=1)

            if self.fecha_fin < timezone.now().date():
                self.tipo_usuario = TipoUsuario.objects.get(nombre='desactivado')
        elif self.plan and Asistencia.objects.filter(usuario=self.user).count() >= self.plan.cantidad_clases:
            self.tipo_usuario = TipoUsuario.objects.get(nombre='desactivado')
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)