from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.lista_base, name='lista_base'),
    path('extra/', views.lista_extra, name='lista_extra'),
    path('sensual/', views.lista_sensual, name='lista_sensual'),
    path('social/', views.lista_social, name='lista_social'),
    path('sensualteam/', views.sensualteam, name='sensualteam'),
    path('socialteam/', views.socialteam, name='socialteam'),
]
