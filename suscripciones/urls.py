from django.urls import path
from . import views  # Asegúrate de importar tus vistas

urlpatterns = [
    # ... tus otras rutas aquí ...

    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('pagos/', views.pagos, name='pagos'),
    path('mis_asistencias/', views.mis_asistencias, name='mis_asistencias'),
]