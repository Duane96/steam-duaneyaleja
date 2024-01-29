from django.shortcuts import render
from .models import Base, Extra, ClaseVistaSensual, ClaseVistaSocial, Tutoriales

def lista_base(request):
    bases = Base.objects.all()
    return render(request, 'reproductor/lista_base.html', {'bases': bases})

def lista_extra(request):
    extras = Extra.objects.all()
    return render(request, 'reproductor/lista_extra.html', {'extras': extras})

def lista_sensual(request):
    clases = ClaseVistaSensual.objects.all()
    return render(request, 'reproductor/lista_sensual.html', {'clases': clases})

def lista_social(request):
    clases = ClaseVistaSocial.objects.all()
    return render(request, 'reproductor/lista_social.html', {'clases': clases})

def sensualteam(request):
    return render(request, 'reproductor/sensualteam.html')

def socialteam(request):
    return render(request, 'reproductor/socialteam.html')

def lista_tutoriales(request):
    clases = Tutoriales.objects.all()
    return render(request, 'reproductor/lista_tutoriales.html', {'clases': clases})