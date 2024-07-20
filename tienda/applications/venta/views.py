from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from applications.venta.models import Sale
from applications.venta.serializer import ReportSalesSerializer


class SalesReport(ListAPIView):
    serializer_class = ReportSalesSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Sale.objects.all()