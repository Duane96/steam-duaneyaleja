from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from .forms import AdminSignupForm, EditarPerfilForm
from suscripciones.models import Perfil
from .models import Pago, Asistencia

from intensivos.models import Intensivo
from intensivos.forms import IntensivoForm

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage  
from core.token import account_activation_token  
from django.contrib.auth.models import User  

from django.contrib.auth import login, authenticate, get_user_model
from django.utils.encoding import force_bytes, force_str    
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from django.db.models import Sum

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from videos.models import Base, Extra, ClaseVistaSensual, ClaseVistaSocial, Tutoriales
from .forms import *
from intensivos.forms import CodigoDescuentoForm

#QR
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt


from .decorators import admin_required
from django.utils.decorators import method_decorator

from django.utils import timezone

from django.db.models import Sum, Q
from django.db.models.functions import TruncDate

from intensivos.models import Intensivo, Participante, CodigoDescuento

from django.shortcuts import render, get_object_or_404



# Create your views here.
@admin_required
def admin(request):
    return render(request, 'administracion/inicio.html')



@admin_required
def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            telefono = form.cleaned_data.get('telefono')
            user.set_password(telefono)  # Establece la contraseña como el número de teléfono
            user.is_active = True
            user.save()  # Guarda el objeto User en la base de datos
            
            perfil, created = Perfil.objects.get_or_create(user=user)
            if not created:
                # Si el perfil ya existe, actualízalo
                perfil.telefono = form.cleaned_data.get('telefono')
                perfil.tipo_usuario = form.cleaned_data.get('tipo_usuario')
                perfil.fecha_inicio = form.cleaned_data.get('fecha_inicio')
                perfil.fecha_fin = form.cleaned_data.get('fecha_fin')
                perfil.tipo_pago = form.cleaned_data.get('tipo_pago')
                perfil.plan = form.cleaned_data.get('plan')
                perfil.save()
            else:
                # Si el perfil es nuevo, establece los campos
                perfil.telefono = form.cleaned_data.get('telefono')
                perfil.tipo_usuario = form.cleaned_data.get('tipo_usuario')
                perfil.fecha_inicio = form.cleaned_data.get('fecha_inicio')
                perfil.fecha_fin = form.cleaned_data.get('fecha_fin')
                perfil.tipo_pago = form.cleaned_data.get('tipo_pago')
                perfil.plan = form.cleaned_data.get('plan')
                perfil.save()
                
             # Aquí es donde podrías crear el pago
            pago = Pago.objects.create(user=user, plan=perfil.plan, fecha_inicio=perfil.fecha_inicio, fecha_fin=perfil.fecha_fin, tipo_pago=perfil.tipo_pago)
            
            # Aquí es donde se crea la asistencia
            Asistencia.objects.create(usuario=user, pago=pago, numero_clase=1)
            
           
  

            # Obtiene la información del sitio actual
            current_site = get_current_site(request)

            # Crea el correo electrónico de activación
            mail_subject = 'STEAM: Cuenta creada'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
            })

            # Envía el correo electrónico de activación
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

            messages.success(request, 'Usuario registrado')
            return redirect('admin_signup')
    else:
        form = AdminSignupForm()
    return render(request, 'administracion/registroadmin.html', {'form': form})



    


#Listado de Usuarios
@admin_required
def user_list(request):
    users = User.objects.order_by('username')
    return render(request, 'administracion/listausuarios.html', {'users': users})


#Eliminar usuarios
@admin_required
def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('lista_usuarios')


#EditarPerfil
@admin_required
def editar_perfil(request, user_id):
    perfil = Perfil.objects.get(user__id=user_id)
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            # Crear un nuevo pago
            pago = Pago.objects.create(
                user=perfil.user,
                plan=perfil.plan,
                fecha_inicio=perfil.fecha_inicio,
                fecha_fin=perfil.fecha_fin,
                tipo_pago=perfil.tipo_pago,
            )
            
             # Guardar explícitamente el pago
            
            
            pago.save()
            
            # Establecer todas las asistencias existentes del usuario como inactivas
            Asistencia.objects.filter(usuario=perfil.user).update(activa=False)

            # Crear una nueva asistencia activa
            Asistencia.objects.create(usuario=perfil.user, pago=pago, numero_clase=1, activa=True)
            
             
            
            # Cambiar el tipo de usuario a 'grupo', 'full', 'cursos' o cualquier otro estado que desees
            perfil.tipo_usuario = TipoUsuario.objects.get(nombre='grupo')  # Asegúrate de que 'grupo' es un nombre válido en tu modelo TipoUsuario
            
            perfil.save()  # Guarda el perfil

            return redirect('lista_usuarios')
    else:
        form = EditarPerfilForm(instance=perfil)
    return render(request, 'administracion/editarperfil.html', {'form': form, 'username': perfil.user.username})





#Suma de montos y muestra de todos los pagos
def normalizar_tipo_pago(tipo_pago):
    # Convierte el tipo de pago a minúsculas
    tipo_pago = tipo_pago.lower()

    # Mapea las diferentes formas de ingresar el tipo de pago a un valor estándar
    if tipo_pago in ['ef', 'efectivo']:
        return 'EF'
    elif tipo_pago in ['tr', 'transferencia']:
        return 'TR'
    else:
        return tipo_pago  # Si no es ninguno de los anteriores, devuelve el valor original

@admin_required
def administracion(request):
    pagos = Pago.objects.all()

    # Normaliza los tipos de pago solo para el propósito de las sumas
    total_efectivo = sum(pago.plan.precio for pago in pagos if normalizar_tipo_pago(pago.tipo_pago) == 'EF')
    total_transferencia = sum(pago.plan.precio for pago in pagos if normalizar_tipo_pago(pago.tipo_pago) == 'TR')

    return render(request, 'administracion/pagos-admin.html', {'pagos': pagos, 'total_efectivo': total_efectivo, 'total_transferencia': total_transferencia})

#Añadir videos
@method_decorator(admin_required, name='dispatch')
class BaseCreateView(CreateView):
    model = Base
    form_class = BaseModelForm
    template_name = 'administracion/base-create.html'  # especifica el nombre de la plantilla aquí
    success_url = reverse_lazy('base-nuevo')  # URL a la que redirigir después de un éxito
    
    def form_valid(self, form):
        messages.success(self.request, 'Agregado correctamente')
        return super().form_valid(form)
   
@method_decorator(admin_required, name='dispatch')
class ExtraCreateView(CreateView):
    model = Extra
    form_class = ExtraModelForm
    template_name = 'administracion/extra-create.html'  # especifica el nombre de la plantilla aquí
    success_url = reverse_lazy('extra-nuevo')  # URL a la que redirigir después de un éxito
    
    def form_valid(self, form):
        messages.success(self.request, 'Agregado correctamente')
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')  
class SensualCreateView(CreateView):
    model = ClaseVistaSensual
    form_class = SensualModelForm
    template_name = 'administracion/sensual-create.html'  # especifica el nombre de la plantilla aquí
    success_url = reverse_lazy('sensual-nuevo')  # URL a la que redirigir después de un éxito
    
    def form_valid(self, form):
        messages.success(self.request, 'Agregado correctamente')
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch') 
class SocialCreateView(CreateView):
    model = ClaseVistaSocial
    form_class = SocialModelForm
    template_name = 'administracion/social-create.html'  # especifica el nombre de la plantilla aquí
    success_url = reverse_lazy('social-nuevo')  # URL a la que redirigir después de un éxito
    
    def form_valid(self, form):
        messages.success(self.request, 'Agregado correctamente')
        return super().form_valid(form)
    
    
    
    
#QR
@admin_required
@csrf_exempt
def registrar_asistencia(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Método no permitido"}, status=405)

    email, dominio = request.POST['qr_data'].split('|')
    if dominio == 'duaneyaleja.com.co':
        usuario = User.objects.get(email=email)
        perfil = Perfil.objects.get(user=usuario)

        # Verificar si el usuario ya está desactivado
        if perfil.tipo_usuario.nombre == 'desactivado':
            # Aquí se ha modificado la línea para devolver el mensaje de error directamente en la respuesta JSON
            return JsonResponse({"message": "Usuario desactivado"}, status=400)

        # Obtener el último pago del usuario
        ultimo_pago = Pago.objects.filter(user=usuario).latest('fecha_inicio')

        # Contar las asistencias asociadas con el último pago
        asistencias_desde_ultimo_pago = Asistencia.objects.filter(usuario=usuario, pago=ultimo_pago).count()

        # Verificar si la fecha_fin es igual a la fecha actual
        if perfil.fecha_fin == timezone.now().date():
            # Aquí se ha modificado la línea para devolver el mensaje de error directamente en la respuesta JSON
            return JsonResponse({"message": "Fecha de plan expirada"}, status=400)

        # Verificar si el usuario tiene clases disponibles
        if ultimo_pago and asistencias_desde_ultimo_pago >= ultimo_pago.plan.cantidad_clases:
            # Aquí se ha modificado la línea para devolver el mensaje de error directamente en la respuesta JSON
            return JsonResponse({"message": "Usuario sin clases disponibles"}, status=400)

        # Registrar la asistencia
        numero_clase = asistencias_desde_ultimo_pago + 1
        Asistencia.objects.create(usuario=usuario, pago=ultimo_pago, numero_clase=numero_clase)  # Asociar la asistencia con el último pago
        messages.success(request, 'Asistencia registrada con éxito')

        return JsonResponse({"message": "Asistencia registrada con éxito"})
    else:
        messages.error(request, 'QR no válido')
        return JsonResponse({"message": "Código QR no válido"}, status=400)







@admin_required    
def asistencia(request):
    return render(request, 'administracion/asistencias.html')


@admin_required
def ver_asistencias(request):
    asistencias = Asistencia.objects.all().order_by('-fecha')
    return render(request, 'administracion/ver-asistencias.html', {'asistencias': asistencias})



def normalizar_tipo_pago_listado(tipo_pago):
    # Convierte el tipo de pago a minúsculas
    tipo_pago = tipo_pago.lower()

    # Mapea las diferentes formas de ingresar el tipo de pago a un valor estándar
    if tipo_pago in ['ef', 'efectivo']:
        return 'EF'
    elif tipo_pago in ['tr', 'transferencia']:
        return 'TR'
    else:
        return tipo_pago  # Si no es ninguno de los anteriores, devuelve el valor original

from django.db.models import Sum, Q, F, Func, Value
from django.db.models.functions import Cast

class Date(Func):
    function = 'DATE'
    template = "%(function)s(%(expressions)s)"

@admin_required
def listado_ingresos_por_fecha(request):
    # Extrae la fecha de la fecha y hora
    pagos = Pago.objects.annotate(fecha=Date('fecha_inicio'))

    # Agrupa los pagos por fecha y calcula la suma de los pagos en efectivo y por transferencia para cada fecha
    pagos = pagos.values('fecha').annotate(total_efectivo=Sum(F('plan__precio'), filter=Q(tipo_pago='EF')))
    pagos = pagos.values('fecha', 'total_efectivo').annotate(total_transferencia=Sum(F('plan__precio'), filter=Q(tipo_pago='TR')))

    return render(request, 'administracion/listado_ingresos.html', {'pagos': pagos})



@method_decorator(admin_required, name='dispatch') 
class TutorialesCreateView(CreateView):
    model = Tutoriales
    form_class = TutorialesModelForm
    template_name = 'administracion/tutorial-create.html'  # especifica el nombre de la plantilla aquí
    success_url = reverse_lazy('tutorial-nuevo')  # URL a la que redirigir después de un éxito
    
    def form_valid(self, form):
        messages.success(self.request, 'Agregado correctamente')
        return super().form_valid(form)



@admin_required
def intensivo_list(request):
    intensivos = Intensivo.objects.order_by('id')
    return render(request, 'administracion/listaintensivo.html', {'intensivos': intensivos})

@admin_required
def intensivo_participantes(request, intensivo_id):
    participantes = Participante.objects.filter(intensivo_id=intensivo_id)

    return render(request, 'administracion/listaintensivo_participantes.html', {'participantes': participantes})





@admin_required
def registro_intensivo(request):
    if request.method == 'POST':
        form = IntensivoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agregado correctamente')
            return redirect('registro_intensivo')
            
    else:
        form = IntensivoForm()
    return render(request, 'administracion/crear-intensivo.html', {'form': form})

@admin_required
def registro_codigo_descuento(request):
    if request.method == 'POST':
        form = CodigoDescuentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Código de descuento agregado correctamente')
            return redirect('registro_codigo_descuento')
    else:
        form = CodigoDescuentoForm()
    return render(request, 'administracion/crear-codigo-descuento.html', {'form': form})


@admin_required
def codigo_descuento_list(request):
    codigos_descuento = CodigoDescuento.objects.order_by('codigo')
    return render(request, 'administracion/listacodigosdescuento.html', {'codigos_descuento': codigos_descuento})

@admin_required
def nuevasclases(request):
    return render(request, 'administracion/nuevasclases.html')

@admin_required
def intensivos(request):
    return render(request, 'administracion/intensivos.html')

@admin_required
def usuarios(request):
    return render(request, 'administracion/usuarios.html')

@admin_required
def centro_asistencias(request):
    return render(request, 'administracion/centro-asistencias.html')


@admin_required
def editar_intensivo(request, intensivo_id):
    intensivo = get_object_or_404(Intensivo, id=intensivo_id)
    if request.method == 'POST':
        form = IntensivoForm(request.POST, instance=intensivo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Actualizado correctamente')
            return redirect('editar_intensivo', intensivo_id=intensivo.id)
    else:
        form = IntensivoForm(instance=intensivo)
    return render(request, 'administracion/editar-intensivo.html', {'form': form})


@admin_required
def eliminar_intensivo(request):
    intensivo_id = request.POST.get('intensivo_id')
    intensivo = get_object_or_404(Intensivo, id=intensivo_id)
    intensivo.delete()
    return redirect('lista_intensivos')

