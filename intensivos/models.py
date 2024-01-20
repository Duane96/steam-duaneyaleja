from django.db import models
from django.forms import ModelForm

class Intensivo(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_evento = models.DateField()
    primera_fecha_pago = models.DateField()
    segunda_fecha_pago = models.DateField()
    lugar = models.CharField(max_length=200)
    precio_primera_fecha_solo = models.DecimalField(max_digits=6, decimal_places=2)
    precio_primera_fecha_pareja = models.DecimalField(max_digits=6, decimal_places=2)
    precio_segunda_fecha_solo = models.DecimalField(max_digits=6, decimal_places=2)
    precio_segunda_fecha_pareja = models.DecimalField(max_digits=6, decimal_places=2)
    precio_especial = models.DecimalField(max_digits=6, decimal_places=2)

class Asistente(models.Model):
    intensivo = models.ForeignKey(Intensivo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    email = models.EmailField()
    viene_en_pareja = models.BooleanField()
    nombre_pareja = models.CharField(max_length=200, blank=True)
    telefono_pareja = models.CharField(max_length=200, blank=True)
    email_pareja = models.EmailField(blank=True)
    comprobante = models.ImageField(upload_to='comprobantes/', blank=True)

class AsistenteForm(ModelForm):
    class Meta:
        model = Asistente
        fields = ['nombre', 'telefono', 'email', 'viene_en_pareja', 'nombre_pareja', 'telefono_pareja', 'email_pareja', 'comprobante']
