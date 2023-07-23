from django.db import models
from django.contrib import admin 

# Create your models here.
class Contribuyente(models.Model):
    num_documento_identificacion = models.CharField(max_length=13, unique = True)
    nombre = models.CharField(max_length=200, null=True, blank=True)
    nombre_comercial = models.CharField(max_length=350, null=True, blank=True)
    actividad_economica = models.CharField(max_length=350, null=True, blank=True)
    estado = models.CharField(max_length=15, null=True, blank=True)
    regimen_pagos = models.CharField(max_length=15, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)

class ContribuyenteAdmin(admin.ModelAdmin):
    list_display = ('num_documento_identificacion', 'nombre', 'nombre_comercial', 'actividad_economica', 
    'estado', 'regimen_pagos', 'fecha')
    search_fields = ['num_documento_identificacion', 'nombre', 'nombre_comercial', 'actividad_economica', 
    'estado', 'regimen_pagos', 'fecha']