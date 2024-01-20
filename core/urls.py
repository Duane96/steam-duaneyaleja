from django.urls import path
from .views import index, signup, activate, home
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('inicio/', home, name='home'),
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    #path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'), 
    path('cambiar-contraseña/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('cambiar-contraseña/hecho/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
]