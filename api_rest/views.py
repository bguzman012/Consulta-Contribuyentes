from django.http import HttpResponse
# import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import *
from datetime import datetime

# import local data
from .serializers import ContribuyenteSerializer
from .models import Contribuyente
from appdivs.models import Client, Petition
from appdivs.utils import *
from datetime import datetime


# create a viewset
class ContribuyenteViewSet(APIView):

    def get(self, request, *args, **kwargs):

        parametros = request.query_params

        # param_tipo = parametros.get('tipo')
        param_busqueda = parametros.get('busqueda')
        param_user = parametros.get('user')

        if len(param_user) == 0:
            return Response({'Error': 'El usuario ingresado no es correcto'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cliente = Client.objects.get(user_cl = str(param_user))
        except Client.DoesNotExist:
            return Response({'Error': 'El usuario ingresado no existe'}, status=status.HTTP_400_BAD_REQUEST)

        if cliente.num_allowed == 0:
             return Response({'Error': 'El usuario se encuentra inactivo, por favor comuniquese con el proveedor para más información'}, status=status.HTTP_400_BAD_REQUEST)
        
        if cliente.num_allowed != -1 and cliente.num_peticiones >= cliente.num_allowed:
            return Response({'Error': 'El usuario ingresado no tiene créditos para obtener información, es necesario revor su suscripción'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_ip = get_ip_address(request)
        petition = Petition(id=None, client = cliente, fecha_peticion=datetime.now().date(), 
                           banco=None, ip_address=str(user_ip))
        petition.save()
        
        cliente.num_peticiones += 1
        cliente.save()
        
        try:
            contribuyente = Contribuyente.objects.get(num_documento_identificacion = str(param_busqueda))
            data_contribuyente = {
                "cedula_rcn": contribuyente.num_documento_identificacion,
                "nombre_razon": contribuyente.nombre,
                "nombre_comercial": contribuyente.nombre_comercial,
                "categoria": "",
                "regimen": contribuyente.regimen_pagos,
                "estado": contribuyente.estado,
                "actividad_economica": contribuyente.actividad_economica,
                "adm_local": "",
                "fecha": contribuyente.fecha
            }
            return Response(data_contribuyente, status=status.HTTP_200_OK)
        
        except Contribuyente.DoesNotExist:

            codigo, data = prepare_data(param_busqueda)

            if codigo == 404:
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            
            if codigo == 400:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            return Response(data, status=status.HTTP_200_OK)
        

class MigracionViewSet(APIView):

    def post(self, request, *args, **kwargs):

        registros_eliminar = Contribuyente.objects.all()

        registros_eliminar.delete()

        nombre_archivo = "DGII_RNC.TXT"

        registros_guardar = leer_archivo_datos(nombre_archivo)

        print(registros_guardar[0])

        Contribuyente.objects.bulk_create(registros_guardar)

        return Response({}, status=status.HTTP_201_CREATED)
