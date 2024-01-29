from django.db import models

class Intensivo(models.Model):
    nombre = models.CharField(max_length=100)
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
