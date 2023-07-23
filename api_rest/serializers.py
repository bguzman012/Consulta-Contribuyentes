from rest_framework import serializers

from .models import Contribuyente

# Create a model serializer
class ContribuyenteSerializer(serializers.HyperlinkedModelSerializer):
    # specify model and fields
    class Meta:
        model = Contribuyente
        fields = ('num_documento_identificacion', 'nombre', 'nombre_comercial', 'actividad_economica', 
    'estado', 'regimen_pagos', 'fecha')