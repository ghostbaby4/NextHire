from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsersSerializer
from drf_yasg.utils import swagger_auto_schema
from Config.utils.pagination import PaginationMixin
from .models import User
from ..permissions import CustomPermission


# Create your views here.
class UsersAPIView(PaginationMixin,APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = User

    @swagger_auto_schema(responses={200: UsersSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las unidades de medida.
        """

        usuarios = User.objects.all().order_by('id')
        page = self.paginate_queryset(usuarios, request)

        if page is not None:
            serializer = UsersSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UsersSerializer(usuarios, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UsersSerializer)
    def post(self, request):
        serializer = UsersSerializer(data=request.data)

        #Validar los datos
        if serializer.is_valid():
            serializer.save() #Creacion del usuario
            return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)
        #En caso de error, retornar las validaciones
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuariosDetails(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = User

    @swagger_auto_schema(responses={200: UsersSerializer})
    def get(self, request, pk):
        """
        Obtener un usuario específico por su ID.
        """
        try:
            usuario = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsersSerializer(usuario)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UsersSerializer, responses={200: UsersSerializer})
    def put(self, request, pk):
        """
        Actualizar completamente una unidad de medida por su ID.
        """
        try:
            usuarios = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, usuarios) #Verificación de permisos
        serializer = UsersSerializer(usuarios, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UsersSerializer, responses={200: UsersSerializer})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un usuario por su ID.
        """
        try:
            usuarios = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, usuarios) #Verificación de permisos
        serializer = UsersSerializer(usuarios, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un usuario por su ID.
        """
        try:
            usuarios = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Usuario encontrado'}, status=status.HTTP_404_NOT_FOUND)

        #self.check_object_permissions(request, usuarios) #Verificación de permisos
        usuarios.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
