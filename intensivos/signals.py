from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from qrcode import QRCode, constants
from .models import Participante  # Asegúrate de que esta importación sea correcta



@receiver(post_save, sender=Participante)
def crear_qr_participante(sender, instance, created, **kwargs):
    if created:
        crear_qr(instance, 'codigo_qr')

def crear_qr_pareja(participante):
    crear_qr(participante, 'codigo_qr_pareja')

def crear_qr(instance, campo_qr):
    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    dominio = f'www.duaneyaleja.com.co/intensivo/{instance.intensivo.id}/'
    datos_qr = f'{instance.correo}|{dominio}'
    qr.add_data(datos_qr)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    temp_handle = BytesIO()
    img.save(temp_handle, format='png')
    temp_handle.seek(0)

    nombre_participante_corto = str(instance.nombre[:100])
    nombre_archivo = 'qrcodes/%s_qr.png' % nombre_participante_corto

    if getattr(instance, campo_qr).storage.exists(nombre_archivo):
        getattr(instance, campo_qr).storage.delete(nombre_archivo)

    getattr(instance, campo_qr).save(nombre_archivo, ContentFile(temp_handle.read()), save=True)
