from datetime import timezone, datetime

from django.db import models
from django.template.defaultfilters import slugify


class Intensivo(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    lugar = models.CharField(max_length=100)
    primera_fecha_pago = models.DateField()
    segunda_fecha_pago = models.DateField()
    fecha_evento = models.DateField()
    precio_primera_fecha_solo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_primera_fecha_pareja = models.DecimalField(max_digits=10, decimal_places=2)
    precio_segunda_fecha_solo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_segunda_fecha_pareja = models.DecimalField(max_digits=10, decimal_places=2)
    precio_promocion = models.DecimalField(max_digits=10, decimal_places=2)
    precio_especial = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

class Participante(models.Model):
    intensivo = models.ForeignKey(Intensivo, on_delete=models.CASCADE, related_name='participantes')
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    viene_en_pareja = models.BooleanField(default=False)
    nombre_pareja = models.CharField(max_length=100, blank=True, null=True)
    correo_pareja = models.EmailField(blank=True, null=True)
    telefono_pareja = models.CharField(max_length=15, blank=True, null=True)
    screenshot_pago = models.ImageField(upload_to='pagos/')
    codigo_qr = models.ImageField(upload_to='intensivo_qrcodes/', blank=True, null=True)
    codigo_qr_pareja = models.ImageField(upload_to='intensivo_qrcodes/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre


class CodigoDescuento(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    intensivo = models.ForeignKey(Intensivo, on_delete=models.CASCADE, related_name='codigos_descuento')
    usos_maximos = models.IntegerField()
    usos_actuales = models.IntegerField(default=0)
    fecha_expiracion = models.DateField()
    precio_descuento = models.DecimalField(max_digits=10, decimal_places=2)

    def esta_vigente(self):
        return datetime.now().date() <= self.fecha_expiracion and self.usos_actuales < self.usos_maximos
    
    def __str__(self):
        return self.codigo
