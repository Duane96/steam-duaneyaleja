from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from suscripciones.models import Plan, TipoUsuario
from suscripciones.models import Perfil

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from videos.models import Base, Extra, ClaseVistaSensual, ClaseVistaSocial

class AdminSignupForm(UserCreationForm):
    telefono = forms.CharField(max_length=20)
    tipo_usuario = forms.ModelChoiceField(queryset=TipoUsuario.objects.all())
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tipo_pago = forms.CharField(max_length=2)
    plan = forms.ModelChoiceField(queryset=Plan.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'telefono', 'tipo_usuario', 'fecha_inicio', 'fecha_fin','tipo_pago', 'plan')
        
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['password1'] = cleaned_data.get('telefono')
        cleaned_data['password2'] = cleaned_data.get('telefono')
        return cleaned_data
    
    def _post_clean(self):
        super()._post_clean()
        # Elimina los errores de los campos de contraseña
        self._errors.pop('password2', None)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'telefono' in self.data:
            self.data = self.data.copy()  # Hace que el QueryDict sea mutable
            self.data['password1'] = self.data['telefono']
            self.data['password2'] = self.data['telefono']
            
            
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['tipo_usuario', 'fecha_inicio', 'fecha_fin', 'plan', 'tipo_pago']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].queryset = Plan.objects.all()
        self.fields['tipo_usuario'].queryset = TipoUsuario.objects.all()


class BaseModelForm(forms.ModelForm):
    class Meta:
        model = Base
        fields = ['nombre', 'descripcion', 'enlace']
        
class ExtraModelForm(forms.ModelForm):
    class Meta:
        model = Extra
        fields = ['nombre', 'descripcion', 'enlace']
        
class SensualModelForm(forms.ModelForm):
    class Meta:
        model = ClaseVistaSensual
        fields = ['nombre', 'descripcion', 'enlace']
        
class SocialModelForm(forms.ModelForm):
    class Meta:
        model = ClaseVistaSocial
        fields = ['nombre', 'descripcion', 'enlace']