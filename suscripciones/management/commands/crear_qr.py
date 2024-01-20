from django.core.management.base import BaseCommand
from suscripciones.models import Perfil
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO

def crear_qr(perfil):
    print("Generando QR para el usuario", perfil.user.username)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(perfil.user.email)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    temp_handle = BytesIO()
    img.save(temp_handle, format='png')
    temp_handle.seek(0)

    # Guarda la imagen en el campo 'codigo_qr'
    try:
        perfil.codigo_qr.save(f'{perfil.user.username}_qr.png', ContentFile(temp_handle.read()), save=True)
        print("Código QR guardado para el usuario", perfil.user.username)
    except Exception as e:
        print("Error al guardar el código QR:", str(e))

class Command(BaseCommand):
    help = 'Crea un código QR para cada perfil de usuario'

    def handle(self, *args, **options):
        self.stdout.write('Ejecutando el comando...')
        for perfil in Perfil.objects.filter(codigo_qr__isnull=True):
            crear_qr(perfil)

