from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Colors, Product

from .serializer import ColorSerializer, ProductSerializer, PaginationSerializer, ProductColorSerializer
from ..venta.viewsets import CustomJSONRenderer


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Colors.objects.all()
    serializer_class = ColorSerializer


class ProductViewSet(viewsets.ModelViewSet):
    renderer_classes = (CustomJSONRenderer,)

    queryset = Product.objects.all()
    serializer_class = ProductColorSerializer
    # permission_classes = (IsAuthenticated,)
    pagination_class = PaginationSerializer

    def perform_create(self, serializer):
        serializer.save(
            user_created=self.request.user,
            video=self.request.data.get('video', "http://yt.com"),
        )

    def list(self, request, *args, **kwargs):
        # queryset = Product.objects.productos_por_user(self.request.user)
        queryset = Product.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
