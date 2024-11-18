from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogos.municipio.models import Municipio
from .serializers import MunicipioSerializer
from drf_yasg.utils import swagger_auto_schema
from Config.utils.pagination import PaginationMixin
from ...seguridad.permissions import CustomPermission
import logging.handlers

logger = logging.getLogger(__name__)

# Create your views here.

class MunicipioAPIView(PaginationMixin, APIView):
    """
    Vista para listar todas los municipios o crear uno nuevo.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Municipio

    @swagger_auto_schema(responses={200: MunicipioSerializer(many=True)})
    def get(self, request):
        """
        Listar todos las municipios.
        """
        logger.info("Get para obtener la lista de todos los Municipios")
        municipio = Municipio.objects.all().order_by('id')
        page = self.paginate_queryset(municipio, request)

        if page is not None:
            serializer = MunicipioSerializer(page, many=True)
            logger.info("Repuesta paginada para Municipio")
            return self.get_paginated_response(serializer.data)

        serializer = MunicipioSerializer(municipio, many=True)
        logger.error("Mostrando todos los Municipios sin paginación")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MunicipioSerializer, responses={201: MunicipioSerializer})
    def post(self, request):
        """
        Crear un nuevo municipio.
        """
        logger.info("Post para crear un nuevo Municipio")
        serializer = MunicipioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Municipio creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el Municipio: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MunicipioDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un municipio específico.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Municipio

    @swagger_auto_schema(responses={200: MunicipioSerializer})
    def get(self, request, pk):

        try:
            municipio = Municipio.objects.get(pk=pk)
        except Municipio.DoesNotExist:
            return Response({'error': 'Municipio no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MunicipioSerializer(municipio)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MunicipioSerializer, responses={200: MunicipioSerializer})
    def put(self, request, pk):
        """
        Actualizar completamente un municipio por su ID.
        """
        logger.info("Solicitud PUT para actualizar Municipio con ID: %s", pk)
        try:
            municipio = Municipio.objects.get(pk=pk)
        except Municipio.DoesNotExist:
            return Response({'error': 'Municipio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, municipio) #Verificación de permisos
        serializer = MunicipioSerializer(municipio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Municipio actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el Municipio con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=MunicipioSerializer, responses={200: MunicipioSerializer})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un municipio por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente Municipio con ID: %s", pk)
        try:
            municipio = Municipio.objects.get(pk=pk)
        except Municipio.DoesNotExist:
            return Response({'error': 'Municipio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, municipio) #Verificación de permisos
        serializer = MunicipioSerializer(municipio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Municipio actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el Municipio con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un municipio por su ID.
        """
        logger.info("Solicitud DELETE para eliminar Municipio con ID: %s", pk)
        try:
            municipio = Municipio.objects.get(pk=pk)
        except Municipio.DoesNotExist:
            return Response({'error': 'Municipio no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, municipio) #Verificación de permisos
        municipio.delete()
        logger.info("Municipio eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)