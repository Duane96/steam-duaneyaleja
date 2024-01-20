from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Perfil  # Asegúrate de importar tu modelo de Perfil
from administracion.models import Pago
from administracion.models import Asistencia

@login_required
def perfil_usuario(request):
    perfil = Perfil.objects.get(user=request.user)  # Obtiene el perfil del usuario actualmente logueado

    context = {
        'perfil': perfil,
    }

    return render(request, 'perfil/perfil.html', context)  # Asegúrate de reemplazar 'perfil.html' con la ruta a tu plantilla


@login_required
def pagos(request):
    perfil = Perfil.objects.get(user=request.user)
    pagos = Pago.objects.filter(user=request.user)
    return render(request, 'perfil/pagos.html', {'perfil': perfil, 'pagos': pagos})

@login_required
def mis_asistencias(request):
    asistencias = Asistencia.objects.filter(usuario=request.user).order_by('-fecha')
    perfil = Perfil.objects.get(user=request.user)
    clases_restantes = perfil.plan.cantidad_clases - asistencias.count()
    return render(request, 'perfil/mis_asistencias.html', {'asistencias': asistencias, 'clases_restantes': clases_restantes, 'fecha_fin': perfil.fecha_fin})
