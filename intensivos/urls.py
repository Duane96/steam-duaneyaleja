from django.urls import path
from . import views

urlpatterns = [
    path('intensivo/<slug:slug>/', views.participante_view, name='intensivo'),
    path('success/', views.registro_exitoso, name='success'),
    path('intensivo/<int:intensivo_id>/verificar_codigo_descuento/', views.verificar_codigo_descuento, name='verificar_codigo_descuento'),
    
]
