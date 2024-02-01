from django.shortcuts import render, redirect
from .forms import ParticipanteForm, IntensivoForm
from .models import Intensivo
from django.utils import timezone

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from .models import Participante, Intensivo, CodigoDescuento
from .signals import crear_qr, crear_qr_pareja

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .pdf_generator import generar_pdf

from django.http import JsonResponse
from django.db.models import F
from django.shortcuts import get_object_or_404


def enviar_correo(participante, request, pdf):
    current_site = get_current_site(request)
    mail_subject = 'Confirmación de registro'
    message = render_to_string('intensivo/correo_plantilla_registro.html', {
        'participante': participante,
        'domain': current_site.domain,
    })
    email = EmailMessage(mail_subject, message, to=[participante.correo])
    email.content_subtype = "html"  # Establece el contenido del correo electrónico como HTML
    email.attach('codigo_qr.pdf', pdf, 'application/pdf')
    email.send()


def participante_view(request, slug):
    # Obtenemos el objeto Intensivo correspondiente al ID proporcionado
    intensivo = get_object_or_404(Intensivo, slug=slug)
    # Obtenemos la fecha actual
    fecha_actual = timezone.now().date()

    # Inicializamos la variable codigo_descuento a None
    codigo_descuento = None

    # Verificamos si el método de la solicitud es POST
    if request.method == 'POST':
        # Creamos una instancia del formulario con los datos enviados en la solicitud
        form = ParticipanteForm(request.POST, request.FILES)
        # Verificamos si el formulario es válido
        if form.is_valid():
            # Obtenemos el código de descuento del formulario
            codigo_ingresado = form.cleaned_data.get('codigo_descuento')
            # Verificamos si se ingresó un código de descuento
            if codigo_ingresado:
                try:
                    # Intentamos obtener el código de descuento del modelo CodigoDescuento
                    codigo = intensivo.codigos_descuento.get(codigo=codigo_ingresado)
                    # Verificamos si el código de descuento está vigente
                    if codigo.esta_vigente():
                        # Si el código de descuento está vigente, lo guardamos en la variable codigo_descuento
                        codigo_descuento = codigo
                        # Incrementamos el número de usos actuales del código de descuento
                        codigo.usos_actuales += 1
                        # Guardamos el código de descuento
                        codigo.save()
                except CodigoDescuento.DoesNotExist:
                    # Si el código de descuento no existe, no hacemos nada
                    pass

            # Creamos una instancia del modelo Participante con los datos del formulario
            participante = form.save(commit=False)
            # Asignamos el objeto Intensivo al participante
            participante.intensivo = intensivo
            # Guardamos el participante
            participante.save()

            # Genera el PDF y lo adjunta al correo electrónico.
            pdf = generar_pdf(participante, 'codigo_qr')
            enviar_correo(participante, request, pdf)

            if participante.viene_en_pareja:
                pareja = Participante(nombre=participante.nombre_pareja, correo=participante.correo_pareja, telefono=participante.telefono_pareja)
                crear_qr_pareja(pareja)
                pdf_pareja = generar_pdf(pareja, 'codigo_qr_pareja')
                enviar_correo(pareja, request, pdf_pareja)

            return redirect('success')
    else:
        form = ParticipanteForm()

    context = {
        'form': form,
        'intensivo': intensivo,
        'codigo_descuento': codigo_descuento,
        'mostrar_seccion_1': fecha_actual <= intensivo.primera_fecha_pago,
        'mostrar_seccion_2': fecha_actual <= intensivo.primera_fecha_pago,
        'mostrar_seccion_3': intensivo.primera_fecha_pago < fecha_actual <= intensivo.segunda_fecha_pago,
        'mostrar_seccion_4': intensivo.primera_fecha_pago < fecha_actual <= intensivo.segunda_fecha_pago,
    }

    return render(request, 'intensivo/registro_participante.html', context)


def registro_intensivo(request):
    if request.method == 'POST':
        form = IntensivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = IntensivoForm()
    return render(request, 'intensivo/registro_intensivo.html', {'form': form})


def registro_exitoso(request):
    
    return render(request, 'intensivo/registro_participante_success.html')


def verificar_codigo_descuento(request, intensivo_id):
    codigo = request.GET.get('codigo', None)
    intensivo = Intensivo.objects.get(id=intensivo_id)
    try:
        codigo_descuento = intensivo.codigos_descuento.get(codigo=codigo)
        es_valido = codigo_descuento.esta_vigente()
        precio_descuento = codigo_descuento.precio_descuento if es_valido else None
    except CodigoDescuento.DoesNotExist:
        es_valido = False
        precio_descuento = None
    data = {
        'es_valido': es_valido,
        'precio_descuento': str(precio_descuento),
    }
    return JsonResponse(data)


