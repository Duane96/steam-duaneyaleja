# suscripciones/signals.py
import os
import qrcode
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from io import BytesIO
from .models import Perfil

@receiver(post_save, sender=Perfil)
def crear_qr(sender, instance, created, **kwargs):
    if created or not instance.codigo_qr:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # Añade el correo electrónico del usuario y el dominio a los datos del QR.
        dominio = 'duaneyaleja.com.co'
        datos_qr = f'{instance.user.email}|{dominio}'
        qr.add_data(datos_qr)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        temp_handle = BytesIO()
        img.save(temp_handle, format='png')
        temp_handle.seek(0)

        # Guarda la imagen en el campo 'codigo_qr'
        instance.codigo_qr.save(os.path.join('qrcodes', f'{instance.user.username}_qr.png'), ContentFile(temp_handle.read()), save=True)