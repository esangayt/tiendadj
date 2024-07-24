from rest_framework import serializers, pagination
from .models import Product, Colors


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PaginationSerializer(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50