from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogos.empresa.models import Empresa
from .serializers import EmpresaSerializer
from drf_yasg.utils import swagger_auto_schema
from Config.utils.pagination import PaginationMixin
from ...seguridad.permissions import CustomPermission
import logging.handlers

logger = logging.getLogger(__name__)

# Create your views here.

class EmpresaAPIView(PaginationMixin, APIView):
    """
    Vista para listar todas las empresas o crear una nueva.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Empresa

    @swagger_auto_schema(responses={200: EmpresaSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las empresas.
        """
        logger.info("Get para obtener la lista de todas las Empresas")
        empresa = Empresa.objects.all().order_by('ID_Empresa')
        page = self.paginate_queryset(empresa, request)

        if page is not None:
            serializer = EmpresaSerializer(page, many=True)
            logger.info("Repuesta paginada para Empresa")
            return self.get_paginated_response(serializer.data)

        serializer = EmpresaSerializer(empresa, many=True)
        logger.error("Mostrando todas las Empresas sin paginación")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EmpresaSerializer, responses={201: EmpresaSerializer})
    def post(self, request):
        """
        Crear una nueva empresa.
        """
        logger.info("Post para crear una nueva Empresa")
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Empresa creada exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear la Empresa: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmpresaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una empresa específica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Empresa

    @swagger_auto_schema(responses={200: EmpresaSerializer})
    def get(self, request, pk):
        """
        Obtener una empresa específica por su ID.
        """
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EmpresaSerializer, responses={200: EmpresaSerializer})
    def put(self, request, pk):
        """
        Actualizar completamente una empresa por su ID.
        """
        logger.info("Solicitud PUT para actualizar Empresa con ID: %s", pk)
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, empresa) #Verificación de permisos
        serializer = EmpresaSerializer(empresa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Empresa actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar la Empresa con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=EmpresaSerializer, responses={200: EmpresaSerializer})
    def patch(self, request, pk):
        """
        Actualizar parcialmente una empresa por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente Empresa con ID: %s", pk)
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, empresa) #Verificación de permisos
        serializer = EmpresaSerializer(empresa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Empresa actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar la Empresa con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una empresa por su ID.
        """
        logger.info("Solicitud DELETE para eliminar Empresa con ID: %s", pk)
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, empresa) #Verificación de permisos
        empresa.delete()
        logger.info("Empresa eliminada exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
