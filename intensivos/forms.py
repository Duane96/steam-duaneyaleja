from django import forms
from .models import Asistente

class AsistenteForm(forms.ModelForm):
    class Meta:
        model = Asistente
        fields = ['nombre', 'telefono', 'email', 'viene_en_pareja', 'nombre_pareja', 'telefono_pareja', 'email_pareja', 'comprobante']
