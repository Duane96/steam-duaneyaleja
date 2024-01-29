from django.urls import path
from . import views

urlpatterns = [
    path('intensivo/<int:intensivo_id>/', views.participante_view, name='intensivo'),
    path('success/', views.registro_exitoso, name='success'),
    
]
