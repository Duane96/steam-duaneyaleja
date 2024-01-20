from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm

  
class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required', 
                             widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Email', 'label': 'Email'}))
    
    class Meta:  
        model = User  
        fields = ('username', 'email', 'password1', 'password2') 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-user'
            if field_name == 'email':
                field.widget.attrs['placeholder'] = 'Email'
            else:
                field.widget.attrs['placeholder'] = field.label
            field.label = ''
            

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir las clases al campo de email
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-user'
            if field_name == 'email':
                field.widget.attrs['placeholder'] = 'Email'
            else:
                field.widget.attrs['placeholder'] = field.label
            field.label = ''
            
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cambiar los nombres de los campos según tus necesidades
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control form-control-user', 'name': 'new_password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control form-control-user', 'name': 'new_password_confirm'})
        
        


class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'bg-light u-full-width'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'bg-light u-full-width'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Mensaje', 'class': 'bg-light u-full-width'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    