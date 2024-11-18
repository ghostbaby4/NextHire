from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogos.cargo.models import Cargo
from .serializers import CargoSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from apps.seguridad.permissions import CustomPermission
from Config.utils.pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

# Create your views here.
class CargoAPIView(PaginationMixin, APIView):
    """
    Vista para listar todos las cargos o crear un nuevo cargo.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Cargo
    @swagger_auto_schema(responses={200: CargoSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los cargos.
        """
        logger.info("Get para obtener la lista de todos los Cargos")
        cargo = Cargo.objects.all().order_by('ID_Cargo')
        page= self.paginate_queryset(cargo, request)

        if page is not None:
            serializer = CargoSerializer(page, many=True)
            logger.info("Repuesta paginada para Cargos")
            return self.get_paginated_response(serializer.data)

        serializer = CargoSerializer(cargo, many=True)
        logger.error("Mostrando todos los cargos sin paginación")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CargoSerializer, responses={201: CargoSerializer})
    def post(self, request):
        """
        Crear un nuevo cargo.
        """
        logger.info("Post para crear un nuevo Cargos")
        serializer = CargoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Cargo creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el cargo: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CargoDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un cargo en específico.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Cargo

    @swagger_auto_schema(responses={200: CargoSerializer})
    def get(self, request, pk):
        """
        Obtener un cargo en específico por su ID.
        """
        try:
            cargo = Cargo.objects.get(pk=pk)
        except Cargo.DoesNotExist:
            return Response({'error': 'Cargo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CargoSerializer(cargo)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CargoSerializer, responses={200: CargoSerializer})
    def put(self, request, pk):
        """
        Actualizar completamente un cargo por su ID.
        """
        logger.info("Solicitud PUT para actualizar cargo con ID: %s", pk)
        try:
            cargo = Cargo.objects.get(pk=pk)
        except Cargo.DoesNotExist:
            return Response({'error': 'Cargo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # self.check_object_permissions(request, cargo) #Verificación de permisos
        serializer = CargoSerializer(cargo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Cargo actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el cargo con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CargoSerializer, responses={200: CargoSerializer})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un cargo por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente cargo con ID: %s", pk)
        try:
            cargo = Cargo.objects.get(pk=pk)
        except Cargo.DoesNotExist:
            return Response({'error': 'Cargo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, cargo) #Verificación de permisos
        serializer = CargoSerializer(cargo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Cargo actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el cargo con ID: %s", pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un cargo por su ID.
        """
        logger.info("Solicitud DELETE para eliminar cargo con ID: %s", pk)
        try:
            cargo = Cargo.objects.get(pk=pk)
        except Cargo.DoesNotExist:
            return Response({'error': 'Cargo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, cargo) #Verificación de permisos
        cargo.delete()
        logger.info("Cargo eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)