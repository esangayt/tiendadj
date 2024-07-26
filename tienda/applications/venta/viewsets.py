from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from applications.producto.models import Product
from applications.venta.models import Sale, SaleDetail
from applications.venta.serializer import ReportSalesSerializer, ProcesoVentaSerializer


class VentasViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = ReportSalesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = Sale.objects.all()
        serializer = ReportSalesSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ProcesoVentaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = 0
        count = 0

        venta = Sale.objects.create(
            date_sale=timezone.now(),
            amount=0,
            count=0,
            type_invoce=serializer.validated_data['type_invoce'],
            type_payment=serializer.validated_data['type_payment'],
            adreese_send=serializer.validated_data['adreese_send'],
            user=self.request.user
        )

        productos = serializer.validated_data['products']

        ventas_detalle = []
        for producto in productos:
            prod = Product.objects.get(id=producto['pk'])
            venta_detalle = SaleDetail(
                sale=venta,
                product=prod,
                count=producto['count'],
                price_purchase=prod.price_purchase,
                price_sale=prod.price_sale
            )

            ventas_detalle.append(venta_detalle)
            amount += prod.price_sale * producto['count']
            count += producto['count']

        venta.amount = amount
        venta.count = count
        venta.save()

        SaleDetail.objects.bulk_create(ventas_detalle)

        return Response({
            'message': 'Venta Registra'
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ReportSalesSerializer(instance)
        return Response(serializer.data)