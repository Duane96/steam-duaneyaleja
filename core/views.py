from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, ContactForm
from django.http import HttpResponse   
from django.contrib.auth import login, authenticate, get_user_model
from django.utils.encoding import force_bytes, force_str    
from django.utils.http import urlsafe_base64_decode

from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage  
from .token import account_activation_token  
from django.contrib.auth.models import User  

from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from django.contrib.auth.views import PasswordChangeView
from .forms import MyPasswordChangeForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')

def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # the form has to be saved in the memory and not in DB
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            
            #This is  to obtain the current cite domain   
            current_site_info = get_current_site(request)  
            mail_subject = 'Duane y Aleja STEAM'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site_info.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Revisa tu correo electronico para activar tu cuenta')  
    else:  
        form = SignupForm()  
    return render(request, 'registration/signup.html', {'form': form})  


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Gracias por activar tu cuenta, ya puedes iniciar sesión')  
    else:  
        return HttpResponse('Enlace de activación invalido.')  
    
    
def index(request):
    return render(request, 'index.html')




def enviar_correo(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Procesar el formulario y enviar el correo
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            # Configura el contenido del correo
            contenido_correo = f'Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}'

            # Configura el envío del correo
            send_mail('Asunto del Correo', contenido_correo, 'tu_email@gmail.com', ['duaneyaleja@gmail.com'])

            # Redirige a una página de éxito o cualquier otra acción después de enviar el correo
            return HttpResponseRedirect('/gracias/')  # Puedes cambiar '/gracias/' según tus necesidades

    else:
        form = ContactForm()

    return render(request, 'index.html', {'form': form})


class MyPasswordChangeView(PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = 'registration/password_change.html'
    success_url = 'password_change_done'



