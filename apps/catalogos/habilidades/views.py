from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HabilidadesSerializer, DetalleHabilidadesSerializer
from .models import Habilidades, DetalleHabilidades, Postulante
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from Config.utils.pagination import PaginationMixin
from ...seguridad.permissions import CustomPermission
import logging.handlers

logger = logging.getLogger(__name__)

class HabilidadesAPIView(PaginationMixin,APIView):
    """
    Vista para listar los tipos de habilidades o crear una nueva habilidad.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Habilidades

    @swagger_auto_schema(responses={200: HabilidadesSerializer()})
    def get(self, request):
        """
        Listar todas las habilidades.
        """
        logger.info("Get para obtener la lista de todas las Habilidades")
        habilidades = Habilidades.objects.all().order_by('ID_Habilidade')
        page = self.paginate_queryset(habilidades, request)

        if page is not None:
            serializer = HabilidadesSerializer(page, many=True)
            logger.info("Repuesta paginada para Habilidades")
            return self.get_paginated_response(serializer.data)

        serializer = HabilidadesSerializer(habilidades, many=True)
        logger.error("Mostrando todas las Habilidades sin paginación")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=HabilidadesSerializer)
    def post(self, request):
        """
        Crear una nuevo tipo de habilidad.
        """
        logger.info("Post para crear una nueva Habilidad")
        serializer = HabilidadesSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    habilidad = Habilidades.objects.create(
                        Codigo=serializer.validated_data['Codigo'],
                        Nombre_Habilidad=serializer.validated_data['Nombre_Habilidad'],
                    )
                    for detalle_data in serializer.validated_data['detalles']:
                        descripcion = detalle_data['Descripcion']
                        postulante = get_object_or_404(Postulante,
                                                       pk=detalle_data['ID_Postulante'].ID_Postulante)
                        DetalleHabilidades.objects.create(
                            Id_Habilidades=habilidad,
                            Descripcion=descripcion,
                            ID_Postulante = postulante
                        )
                habilidad_serializer = HabilidadesSerializer(habilidad)
                logger.info("Habilidad creada exitosamente")
                return Response(habilidad_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error("No se pudo crear la Habilidad: %s", serializer.errors)
                # Devuelve un error en caso de excepción
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetalleHabilidadDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un tipo de habilidad específica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Habilidades

    @swagger_auto_schema(responses={200: HabilidadesSerializer()})
    def get(self, request, pk):
        """
        Obtener una habilidad específica por su ID.
        """
        habilidad = get_object_or_404(Habilidades, pk=pk)
        serializer = HabilidadesSerializer(habilidad)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        """
        Eliminar una habilidad por su ID.
        """
        logger.info("Solicitud DELETE para eliminar Habilidad con ID: %s", pk)
        habilidad = get_object_or_404(Habilidades, pk=pk)
        try:
            with transaction.atomic():
                #self.check_object_permissions(request, habilidad) #Verificación de permisos
                DetalleHabilidades.objects.filter(Id_Habilidades=habilidad).delete()
                habilidad.delete()
                logger.info("Habilidad eliminada exitosamente con ID: %s", pk)
            return Response({"message": "Habilidad eliminada con éxito."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)