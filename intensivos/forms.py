from django import forms
from .models import Participante, Intensivo

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nombre', 'correo', 'telefono', 'viene_en_pareja', 'nombre_pareja', 'correo_pareja', 'telefono_pareja', 'screenshot_pago']

class IntensivoForm(forms.ModelForm):
    
    primera_fecha_pago = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    segunda_fecha_pago = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_evento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Intensivo
        fields = ['nombre', 'lugar', 'primera_fecha_pago', 'segunda_fecha_pago', 'fecha_evento', 'precio_primera_fecha_solo', 'precio_primera_fecha_pareja', 'precio_segunda_fecha_solo', 'precio_segunda_fecha_pareja', 'precio_promocion', 'precio_especial']
