from django.urls import path
from .views import admin, admin_signup, user_list, delete_user, editar_perfil, administracion, asistencia, ver_asistencias
from .views import BaseCreateView, ExtraCreateView, SensualCreateView, SocialCreateView, registrar_asistencia


urlpatterns = [
    path('inicioadmin/', admin, name="inicio_admin"),
    path('admin-signup/', admin_signup, name='admin_signup'),
    path('lista-usuarios/', user_list, name='lista_usuarios'),
    path('eliminar-usuario/<int:user_id>/', delete_user, name='delete_user'),
    path('editar_perfil/<int:user_id>/', editar_perfil, name='editar_perfil'),
    path('pagos-admin', administracion, name="pagos_admin" ),
    path('base/nuevo/', BaseCreateView.as_view(), name='base-nuevo'),
    path('extra/nuevo/', ExtraCreateView.as_view(), name='extra-nuevo'),
    path('sensual/nuevo', SensualCreateView.as_view(), name='sensual-nuevo'),
    path('social/nuevo', SocialCreateView.as_view(), name='social-nuevo'),
    path('procesar_qr/', registrar_asistencia, name='procesar_qr'),
    path('asistencias/', asistencia, name='asistencia'),
    path('ver_asistencias/', ver_asistencias, name='ver_asistencias'),
    
]