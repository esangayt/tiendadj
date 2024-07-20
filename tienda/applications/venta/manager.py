from django.db import models


class SaleManager(models.Manager):
    def productos_por_venta(self, sale):
        return self.filter(sale=sale)
