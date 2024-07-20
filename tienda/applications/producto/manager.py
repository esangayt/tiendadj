from django.db import models

class ProductManager(models.Manager):
    def productos_por_user(self, usuario):
        return self.filter(user_created=usuario)

    def productos_stock_valid(self):
        return self.filter(stock__gt=0)