from django.shortcuts import render, redirect
from .forms import ParticipanteForm, IntensivoForm
from .models import Intensivo
from django.utils import timezone

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from .models import Participante
from .signals import crear_qr, crear_qr_pareja

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .pdf_generator import generar_pdf

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


def participante_view(request, intensivo_id):
    intensivo = Intensivo.objects.get(id=intensivo_id)
    fecha_actual = timezone.now().date()

    if request.method == 'POST':
        form = ParticipanteForm(request.POST, request.FILES)
        if form.is_valid():
            participante = form.save(commit=False)
            participante.intensivo = intensivo
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

