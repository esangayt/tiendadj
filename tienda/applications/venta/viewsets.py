from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone

from applications.producto.models import Product
from applications.producto.serializer import PaginationSerializer
from applications.venta.models import Sale, SaleDetail
from applications.venta.serializer import ReportSalesSerializer, ProcesoVentaSerializer

class VentasViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = ReportSalesSerializer
    # renderer_classes = (CustomJSONRenderer,)
    # parser_classes  = [ResponseManager]
    # permission_classes = [IsAuthenticated]
    pagination_class = PaginationSerializer
    authentication_classes = [TokenAuthentication]  # clase general que solo identifica al usuario

    def handle_exception(self, exc):
        # response_manager = ResponseManager(self.request)
        # return response_manager.catch(exc)
        return super(VentasViewSet, self).handle_exception(exc)


    def finalize_response(self, request, response, *args, **kwargs):
        # add atytribute test = false in response at begin of response
        response = super(VentasViewSet, self).finalize_response(request, response, *args, **kwargs)

        # response_manager = ResponseManager(request)
        #
        # if isinstance(response, Exception):
        #     return response_manager.catch(response)
        #
        # # Cualquier lógica personalizada aquí, por ejemplo, manejo de errores
        # if response.status_code >= 400:
        #     return response_manager.catch(response.data)
        #
        # # Respuesta estándar
        # content = response.data if response.status_code < 400 else None
        # message = response.data.get("detail", "") if response.status_code >= 400 else ""
        # res = response_manager.response(content, response.status_code, message)
        # response.data = res.data

        return response

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:  # create, update, partial_update, destroy
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

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

    # def retrieve(self, request, *args, **kwargs):
    #     print(kwargs['pk'])
    #
    #     instance = get_object_or_404(Sale, pk=kwargs['pk'])
    #     serializer = ReportSalesSerializer(instance)
    #     return Response(serializer.data)
