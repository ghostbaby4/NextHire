from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogos.departamentos.models import Departamento
from .serializers import DepartamentoSerializer
from drf_yasg.utils import swagger_auto_schema
from Config.utils.pagination import PaginationMixin
from ...seguridad.permissions import CustomPermission
import logging.handlers

logger = logging.getLogger(__name__)

# Create your views here.

class DepartamentoAPIView(PaginationMixin, APIView):
    """
    Vista para listar todos los departamentos o crear uno nuevo.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Departamento

    @swagger_auto_schema(responses={200: DepartamentoSerializer(many=True)})
    def get(self, request):
        """
         Listar todos los departamentos.
         """
        logger.info("Get para obtener la lista de todos los Departamentos")
        departamento = Departamento.objects.all().order_by('ID_Departamento')
        page = self.paginate_queryset(departamento, request)

        if page is not None:
            serializer = DepartamentoSerializer(page, many=True)
            logger.info("Repuesta paginada para Departamentos")
            return self.get_paginated_response(serializer.data)

        serializer = DepartamentoSerializer(departamento, many=True)
        logger.error("Mostrando todos los Departamentos sin paginación")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DepartamentoSerializer, responses={201: DepartamentoSerializer})
    def post(self, request):
        """
        Crear un nuevo departamento.
        """
        logger.info("Post para crear un nuevo Departamento")
        serializer = DepartamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Departamento creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el Departamento: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartamentoDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un departamento en específico.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Departamento

    @swagger_auto_schema(responses={200: DepartamentoSerializer})
    def get(self, request, pk):
        """
        Obtener un departamento en específico por su ID.
        """
        try:
            departamento = Departamento.objects.get(pk=pk)
        except Departamento.DoesNotExist:
            return Response({'error': 'Departamento no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartamentoSerializer(departamento)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DepartamentoSerializer, responses={200: DepartamentoSerializer})
    def put(self, request, pk):
        """
        Actualizar completamente un departamento por su ID.
        """
        logger.info("Solicitud PUT para actualizar Departamento con ID: %s", pk)
        try:
            departamento = Departamento.objects.get(pk=pk)
        except Departamento.DoesNotExist:
            return Response({'error': 'Departamento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, departamento) #Verificación de permisos
        serializer = DepartamentoSerializer(departamento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Departamento actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el Departamento con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=DepartamentoSerializer, responses={200: DepartamentoSerializer})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un departamento por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente Departamento con ID: %s", pk)
        try:
            departamento = Departamento.objects.get(pk=pk)
        except Departamento.DoesNotExist:
            return Response({'error': 'Departamento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, departamento) #Verificación de permisos
        serializer = DepartamentoSerializer(departamento, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Departamento actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el Departamento con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un departamento por su ID.
        """
        logger.info("Solicitud DELETE para eliminar Departamento con ID: %s", pk)
        try:
            departamento = Departamento.objects.get(pk=pk)
        except Departamento.DoesNotExist:
            return Response({'error': 'Departamento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, departamento) #Verificación de permisos
        departamento.delete()
        logger.info("Departamento eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)