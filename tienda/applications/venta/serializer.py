from rest_framework import serializers

from applications.venta.models import Sale, SaleDetail


class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = '__all__'


class ReportSalesSerializer(serializers.ModelSerializer):
    detalle_venta = serializers.SerializerMethodField(
        method_name='get_detalle_venta',
        read_only=True
    )

    class Meta:
        model = Sale

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.Meta.fields = self.get_structure()

    def get_detalle_venta(self, obj):
        detalle = SaleDetail.objects.productos_por_venta(obj)
        return SaleDetailSerializer(detalle, many=True).data

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     detalle = SaleDetail.objects.productos_por_venta(instance)
    #     data['detalle_venta'] = SaleDetailSerializer(detalle, many=True).data
    #     return data

    @staticmethod
    def get_structure():
        return [
            'id',
            'date_sale',
            'amount',
            'count',
            'type_invoce',
            'cancelado',
            'type_payment',
            'state',
            'adreese_send',
            'anulate',
            'user',
            'detalle_venta'
        ]


class ProductoDetailSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    count = serializers.IntegerField()


class ProcesoVentaSerializer(serializers.Serializer):
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    products = ProductoDetailSerializer(many=True)


### new way to add sale
class ArrayIntegerListSerializer(serializers.ListField):
    child = serializers.IntegerField()

class ProcesoVentaSerializer2(serializers.Serializer):
    type_invoce = serializers.IntegerField()
    type_payment = serializers.IntegerField()
    adreese_send = serializers.CharField()
    products = ArrayIntegerListSerializer()
    cantidades = ArrayIntegerListSerializer()
