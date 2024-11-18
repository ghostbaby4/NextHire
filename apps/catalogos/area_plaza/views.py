from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogos.area_plaza.models import AreaPlaza
from .serializers import AreaPlazaSerializer
from drf_yasg.utils import swagger_auto_schema
from Config.utils.pagination import PaginationMixin
from ...seguridad.permissions import CustomPermission
import logging.handlers

logger = logging.getLogger(__name__)

# Create your views here.
class ArePlazaAPIView(PaginationMixin, APIView):
    """
    Vista para listar todas las areas de plaza o crear una nueva.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = AreaPlaza

    @swagger_auto_schema(responses={200: AreaPlazaSerializer(many=True)})
    def get(self, request):
        """
              Listar todas las areas plazas.
        """
        logger.info("Get para obtener la lista de todas los área plazas")
        areaplaza = AreaPlaza.objects.all().order_by('ID_AreaPLAZA')
        page = self.paginate_queryset(areaplaza, request)

        if page is not None:
            serializer = AreaPlazaSerializer(page, many=True)
            logger.info("Repuesta paginada para área plaza")
            return self.get_paginated_response(serializer.data)

        serializer = AreaPlazaSerializer(areaplaza, many=True)
        logger.error("Mostrando todos las área plazas sin paginación")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AreaPlazaSerializer, responses={201: AreaPlazaSerializer})
    def post(self, request):
        """
        Crear una nueva area plaza.
        """
        logger.info("Post para crear una nueva área plaza")
        serializer = AreaPlazaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Área plaza creada exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el área plaza: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AreaPlazaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una area plaza específica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = AreaPlaza

    @swagger_auto_schema(responses={200: AreaPlazaSerializer})
    def get(self, request, pk):
        """
        Obtener una area plaza específica por su ID.
        """
        try:
            areaplaza = AreaPlaza.objects.get(pk=pk)
        except AreaPlaza.DoesNotExist:
            return Response({'error': 'Área de plaza no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AreaPlazaSerializer(areaplaza)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AreaPlazaSerializer, responses={200: AreaPlazaSerializer})
    def put(self, request, pk):
        """
        Actualizar completamente una area plaza por su ID.
        """
        logger.info("Solicitud PUT para actualizar área plaza con ID: %s", pk)
        try:
            areaplaza = AreaPlaza.objects.get(pk=pk)
        except AreaPlaza.DoesNotExist:
            return Response({'error': 'Área de plaza no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, areaplaza) #Verificación de permisos
        serializer = AreaPlazaSerializer(areaplaza, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Área plaza actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el área plaza con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AreaPlazaSerializer, responses={200: AreaPlazaSerializer})
    def patch(self, request, pk):
        """
        Actualizar parcialmente una área plaza por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente área plaza con ID: %s", pk)
        try:
            areaplaza = AreaPlaza.objects.get(pk=pk)
        except AreaPlaza.DoesNotExist:
            return Response({'error': 'Área de plaza no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, areaplaza) #Verificación de permisos
        serializer = AreaPlazaSerializer(areaplaza, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Área plaza actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el área plaza con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una área plaza por su ID.
        """
        logger.info("Solicitud DELETE para eliminar área plaza con ID: %s", pk)
        try:
            areaplaza = AreaPlaza.objects.get(pk=pk)
        except AreaPlaza.DoesNotExist:
            return Response({'error': 'Área de plaza no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, areaplaza) #Verificación de permisos
        areaplaza.delete()
        logger.info("Área plaza eliminada exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)