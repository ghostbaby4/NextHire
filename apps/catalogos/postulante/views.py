from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostulanteSerializer, DetallePostulanteSerializer
from .models import Postulante, DetallePostulante, Municipio, Profesion
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from ..plaza.models import DetallePlaza
from Config.utils.pagination import PaginationMixin
from ...seguridad.permissions import CustomPermission
import logging.handlers

logger = logging.getLogger(__name__)

class PostulanteAPIView(PaginationMixin,APIView):
    """
    Vista para listar los tipos de postulantes o crear un nuevo postulante.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Postulante

    @swagger_auto_schema(responses={200: PostulanteSerializer()})
    def get(self, request):
        """
        Listar todos los Postulantes.
        """
        logger.info("Get para obtener la lista de todos los Postulantes")
        postulante = Postulante.objects.all().order_by('ID_Postulante')
        page = self.paginate_queryset(postulante, request)

        if page is not None:
            serializer = PostulanteSerializer(page, many=True)
            logger.info("Repuesta paginada para Postulantes")
            return self.get_paginated_response(serializer.data)

        serializer = PostulanteSerializer(postulante, many=True)
        logger.error("Mostrando todos los Postulantes sin paginación")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PostulanteSerializer)
    def post(self, request):
        """
        Crear una nuevo postulante.
        """
        logger.info("Post para crear un nuevo Postulante")
        serializer = PostulanteSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    municipio = get_object_or_404(Municipio, pk=serializer.validated_data['ID_Municipio'].id)
                    profesion = get_object_or_404(Profesion, pk=serializer.validated_data['ID_Profesion'].ID_Profesion)
                    postulante = Postulante.objects.create(
                        Cedula=serializer.validated_data['Cedula'],
                        Nombre_Postulante=serializer.validated_data['Nombre_Postulante'],
                        Apellidos=serializer.validated_data['Apellidos'],
                        Sexo=serializer.validated_data['Sexo'],
                        Correo=serializer.validated_data['Correo'],
                        Telefono=serializer.validated_data['Telefono'],
                        Fecha_Nacimiento=serializer.validated_data['Fecha_Nacimiento'],
                        Direccion=serializer.validated_data['Direccion'],
                        Experiencia_Laboral=serializer.validated_data['Experiencia_Laboral'],
                        ID_Municipio=municipio,
                        ID_Profesion=profesion
                    )
                    for detalle_data in serializer.validated_data['detalles']:
                        comentarios = detalle_data['Comentarios']
                        detalleplaza = get_object_or_404(DetallePlaza,
                                                       pk=detalle_data['ID_DetallePlaza'].ID_DetallePlaza)
                        DetallePostulante.objects.create(
                            ID_Postulante=postulante,
                            ID_DetallePlaza=detalleplaza,
                            Comentarios=comentarios
                        )

                postulante_serializer = PostulanteSerializer(postulante)
                logger.info("Postulante creado exitosamente")
                return Response(postulante_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error("No se pudo crear el Postulante: %s", serializer.errors)
                # Devuelve un error en caso de excepción
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetallePostulanteDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un postulante específico.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Postulante

    @swagger_auto_schema(responses={200: PostulanteSerializer()})
    def get(self, request, pk):
        """
        Obtener un postulante específico por su ID.
        """
        postulante = get_object_or_404(Postulante, pk=pk)
        serializer = PostulanteSerializer(postulante)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        """
        Eliminar un postulante por su ID.
        """
        logger.info("Solicitud DELETE para eliminar Postulante con ID: %s", pk)
        postulante = get_object_or_404(Postulante, pk=pk)
        try:
            with transaction.atomic():
                #self.check_object_permissions(request, postulante) #Verificación de permisos
                DetallePostulante.objects.filter(ID_Postulante=postulante).delete()
                postulante.delete()
                logger.info("Postulante eliminado exitosamente con ID: %s", pk)
            return Response({"message": "Postulante eliminado con éxito."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)