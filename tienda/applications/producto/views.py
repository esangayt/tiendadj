from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication

# Create your views here.
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from applications.producto.models import Product
from applications.producto.serializer import ProductSerializer
from applications.users.models import User


class ListProductUserAPI(ListAPIView):
    serializer_class = ProductSerializer
    #solo caraga la vista si el token es valido
    #lanza errores si no esta autenticado
    permission_classes = (IsAuthenticated, IsAdminUser)
    #identifica y auhtentica al usuario
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        # return self.request.user.productos.all()
        # return Product.objects.all()
        return Product.objects.productos_por_user(self.request.user)


class ListProductPorGeneroAPI(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def handle_exception(self, exc):
        # Personaliza la respuesta de error en formato JSON
        return Response({"error": str(exc)}, status=400)
    def get_queryset(self):
        genero = self.kwargs['gender']
        return Product.objects.productos_por_genero(genero)


class FiltrarProductos(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def handle_exception(self, exc):
        # Personaliza la respuesta de error en formato JSON
        return Response({"error": str(exc)}, status=400)

    def get_queryset(self):
        man = self.request.query_params.get('man', None)
        woman = self.request.query_params.get('woman', None)
        name = self.request.query_params.get('name', None)
        print(man)
        return Product.objects.productos_por_filter(
            man=man,
            woman=woman,
            name=name
        )