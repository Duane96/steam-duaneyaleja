from django.utils import timezone
from .models import Perfil
from administracion.models import Asistencia, Pago

def clases_disponibles(request):
    # Solo añade las variables si el usuario está autenticado
    if request.user.is_authenticated:
        usuario = request.user
        perfil = Perfil.objects.get(user=usuario)

        # Comprueba si el usuario tiene al menos un Pago
        if Pago.objects.filter(user=usuario).exists():
            # Si el usuario tiene al menos un Pago, obtén el último
            ultimo_pago = Pago.objects.filter(user=usuario).latest('fecha_inicio')

            # Cuenta las asistencias asociadas con el último pago
            asistencias_desde_ultimo_pago = Asistencia.objects.filter(usuario=usuario, pago=ultimo_pago).count()

            # Determina si el usuario tiene clases disponibles
            tiene_clases_disponibles = ultimo_pago and asistencias_desde_ultimo_pago < ultimo_pago.plan.cantidad_clases
        else:
            # Si el usuario no tiene ningún Pago, no tiene clases disponibles
            tiene_clases_disponibles = False

        # Determina si la fecha_fin es menor que la fecha actual
        es_fecha_fin = perfil.fecha_fin < timezone.now().date()

        return {
            'tiene_clases_disponibles': tiene_clases_disponibles,
            'es_fecha_fin': es_fecha_fin,
        }
    else:
        return {}
