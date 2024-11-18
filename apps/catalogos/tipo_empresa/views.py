from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogos.tipo_empresa.models import TipoEmpresa
from .serializers import TipoEmpresaSerializer
from drf_yasg.utils import swagger_auto_schema
from Config.utils.pagination import PaginationMixin
from ...seguridad.permissions import CustomPermission
import logging.handlers

logger = logging.getLogger(__name__)

# Create your views here.
class TipoEmpresaAPIView(PaginationMixin, APIView):
    """
    Vista para listar los tipos de empresa o crear un nuevo tipo de empresa.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = TipoEmpresa

    @swagger_auto_schema(responses={200: TipoEmpresaSerializer(many=True)})
    def get(self, request):
        """
        Listar los tipos de empresa.
        """
        logger.info("Get para obtener la lista de todos los Tipos de Empresas")
        tipoempresa = TipoEmpresa.objects.all().order_by('ID_TipoEmpresa')
        page = self.paginate_queryset(tipoempresa, request)

        if page is not None:
            serializer = TipoEmpresaSerializer(page, many=True)
            logger.info("Repuesta paginada para Tipos de Empresas")
            return self.get_paginated_response(serializer.data)

        serializer = TipoEmpresaSerializer(tipoempresa, many=True)
        logger.error("Mostrando todos los Tipos de Empresas sin paginación")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TipoEmpresaSerializer, responses={201: TipoEmpresaSerializer})
    def post(self, request):
        """
        Crear una nuevo tipo de empresa.
        """
        logger.info("Post para crear un nuevo Tipo de Empresa")
        serializer = TipoEmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tipo de Empresa creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el Tipo de Empresa: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TipoEmpresaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un tipo de empresa específica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = TipoEmpresa

    @swagger_auto_schema(responses={200: TipoEmpresaSerializer})
    def get(self, request, pk):
        """
        Obtener un tipo de empresa específica por su ID.
        """
        try:
            tipoempresa = TipoEmpresa.objects.get(pk=pk)
        except TipoEmpresa.DoesNotExist:
            return Response({'error': 'Tipo de empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TipoEmpresaSerializer(tipoempresa)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TipoEmpresaSerializer, responses={200: TipoEmpresaSerializer})
    def put(self, request, pk):
        """
        Actualizar completamente un tipo de empresa por su ID.
        """
        logger.info("Solicitud PUT para actualizar Tipo de Empresa con ID: %s", pk)
        try:
            tipoempresa = TipoEmpresa.objects.get(pk=pk)
        except TipoEmpresa.DoesNotExist:
            return Response({'error': 'Tipo de empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, tipoempresa) #Verificación de permisos
        serializer = TipoEmpresaSerializer(tipoempresa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tipo de Empresa actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el Tipo de Empresa con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TipoEmpresaSerializer, responses={200: TipoEmpresaSerializer})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un tipo empresa por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente Tipo de Empresa con ID: %s", pk)
        try:
            tipoempresa = TipoEmpresa.objects.get(pk=pk)
        except TipoEmpresa.DoesNotExist:
            return Response({'error': 'Tipo de empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, tipoempresa) #Verificación de permisos
        serializer = TipoEmpresaSerializer(tipoempresa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tipo de Empresa actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el Tipo de Empresa con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un tipo de empresa por su ID.
        """
        logger.info("Solicitud DELETE para eliminar Tipo de Empresa con ID: %s", pk)
        try:
            tipoempresa = TipoEmpresa.objects.get(pk=pk)
        except TipoEmpresa.DoesNotExist:
            return Response({'error': 'Mascota no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, tipoempresa) #Verificación de permisos
        tipoempresa.delete()
        logger.info("Tipo de Empresa eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)