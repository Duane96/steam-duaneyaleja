from django.db import models

class Base(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    enlace = models.URLField()
    
    def __str__(self):
        return self.nombre

class Extra(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    enlace = models.URLField()
    
    def __str__(self):
        return self.nombre

class ClaseVistaSensual(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    enlace = models.URLField()
    
    def __str__(self):
        return self.nombre

class ClaseVistaSocial(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    enlace = models.URLField()
    
    def __str__(self):
        return self.nombre
    
    
class Tutoriales(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    enlace = models.URLField()
    
    def __str__(self):
        return self.nombre