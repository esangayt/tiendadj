from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404

from applications.producto.ManagerResponse import ResponseManager
from applications.producto.models import Product
from applications.venta.models import Sale, SaleDetail
from applications.venta.serializer import ReportSalesSerializer, ProcesoVentaSerializer


class VentasViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = ReportSalesSerializer
    # permission_classes = [IsAuthenticated]
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

    def retrieve(self, request, *args, **kwargs):
        print(kwargs['pk'])

        instance = get_object_or_404(Sale, pk=kwargs['pk'])
        serializer = ReportSalesSerializer(instance)
        return Response(serializer.data)

    def exception_handler(exc, context):
        """
        Returns the response that should be used for any given exception.

        By default we handle the REST framework `APIException`, and also
        Django's built-in `Http404` and `PermissionDenied` exceptions.

        Any unhandled exceptions may return `None`, which will cause a 500 error
        to be raised.
        """
        if isinstance(exc, Http404):
            exc = exceptions.NotFound(*(exc.args))
        elif isinstance(exc, PermissionDenied):
            exc = exceptions.PermissionDenied(*(exc.args))

        if isinstance(exc, exceptions.APIException):
            headers = {}
            if getattr(exc, 'auth_header', None):
                headers['WWW-Authenticate'] = exc.auth_header
            if getattr(exc, 'wait', None):
                headers['Retry-After'] = '%d' % exc.wait

            if isinstance(exc.detail, (list, dict)):
                print("ahora estoy")
                data = exc.detail
            else:
                print("ahora no")
                data = {'detail': exc.detail}

            # print(exc.detail.get('type_invoce')[0])
            # print(exc.get_full_details())
            # print(exc.get_codes())
            # print(exc.with_traceback())
            # print(traceback.print_exc())
            # print(traceback.format_stack()
            # print(sys.exception())
            # print(traceback.format_list())
            # print(traceback.extract_stack(exc))
            # print(traceback.format_per())

            # exc_type, exc_value, exc_tb = exc.__class__, exc, exc.__traceback__
            trace_list = traceback.format_exception(sys.exception(), limit=None, chain=True)
            # print(traceback.format_exception_only(sys.exception()))
            print(exc.get_full_details())

            schema = {
                "error": 200 >= exc.status_code < 300,
                "message": exc.get_full_details(),
                "code": exc.status_code,
                "data": None,
            }

            if settings.DEBUG:
                schema["debug"] = {
                    "type": type(exc).__name__,
                    "details": traceback.format_exception_only(sys.exception()),
                    # "args": exc.args,
                    # "traceback": traceback.format_per(),
                    "traceback": trace_list,
                }
            set_rollback()
            return Response(schema, status=exc.status_code, headers=headers)

        return None
