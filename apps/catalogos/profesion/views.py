from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogos.profesion.models import Profesion
from .serializers import ProfesionSerializer
from drf_yasg.utils import swagger_auto_schema
from Config.utils.pagination import PaginationMixin
from ...seguridad.permissions import CustomPermission
import logging.handlers

logger = logging.getLogger(__name__)

# Create your views here.
class ProfesionAPIView(PaginationMixin, APIView):
    """
    Vista para listar todas las profesiones o crear una nueva.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Profesion

    @swagger_auto_schema(responses={200: ProfesionSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las profesiones.
        """
        logger.info("Get para obtener la lista de todas las profesiones")
        profesion = Profesion.objects.all().order_by('ID_Profesion')
        page = self.paginate_queryset(profesion, request)

        if page is not None:
            serializer = ProfesionSerializer(page, many=True)
            logger.info("Repuesta paginada para Profesiones")
            return self.get_paginated_response(serializer.data)

        serializer = ProfesionSerializer(profesion, many=True)
        logger.error("Mostrando todas las Profesiones sin paginación")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProfesionSerializer, responses={201: ProfesionSerializer})
    def post(self, request):
        """
        Crear una nueva profesión.
        """
        logger.info("Post para crear una nueva Profesión")
        serializer = ProfesionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Profesión creada exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear la Profesión: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfesionDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una profesión específica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Profesion

    @swagger_auto_schema(responses={200: ProfesionSerializer})
    def get(self, request, pk):
        """
        Obtener una profesión específica por su ID.
        """
        try:
            profesion = Profesion.objects.get(pk=pk)
        except Profesion.DoesNotExist:
            return Response({'error': 'Profesión no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfesionSerializer(profesion)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProfesionSerializer, responses={200: ProfesionSerializer})
    def put(self, request, pk):
        """
        Actualizar completamente una profesión por su ID.
        """
        logger.info("Solicitud PUT para actualizar Profesión con ID: %s", pk)
        try:
            profesion = Profesion.objects.get(pk=pk)
        except Profesion.DoesNotExist:
            return Response({'error': 'Profesión no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, profesion) #Verificación de permisos
        serializer = ProfesionSerializer(profesion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Profesión actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar la Profesión con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProfesionSerializer, responses={200: ProfesionSerializer})
    def patch(self, request, pk):
        """
        Actualizar parcialmente una profesión por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente Profesión con ID: %s", pk)
        try:
            profesion = Profesion.objects.get(pk=pk)
        except Profesion.DoesNotExist:
            return Response({'error': 'Profesión no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, profesion) #Verificación de permisos
        serializer = ProfesionSerializer(profesion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Profesión actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar la Profesión con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una profesión por su ID.
        """
        logger.info("Solicitud DELETE para eliminar Profesión con ID: %s", pk)
        try:
            profesion = Profesion.objects.get(pk=pk)
        except Profesion.DoesNotExist:
            return Response({'error': 'Profesión no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        #self.check_object_permissions(request, profesion) #Verificación de permisos
        profesion.delete()
        logger.info("Profesión eliminada exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)