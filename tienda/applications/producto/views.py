from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication

# Create your views here.
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from applications.producto.models import Product
from applications.producto.serializer import ProductSerializer
from applications.users.models import User


class ListProductUserAPI(ListAPIView):
    serializer_class = ProductSerializer
    #solo caraga la vista si el token es valido
    #lanza errores si no esta autenticado
    permission_classes = (IsAuthenticated,)
    #identifica y auhtentica al usuario
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        # return self.request.user.productos.all()
        # return Product.objects.all()
        return Product.objects.productos_por_user(self.request.user)

