from django.db import models


class ProductManager(models.Manager):
    def productos_por_user(self, usuario):
        return self.filter(user_created=usuario)

    def productos_stock_valid(self):
        return self.filter(stock__gt=0)

    def productos_por_genero(self, genero):
        if genero == 'm':
            mujer = True
            varon = False
        elif genero == 'v':
            mujer = False
            varon = True
        else:
            mujer = True
            varon = True

        return self.filter(woman=mujer, man=varon).order_by('created')

    def productos_por_filter(self, **filters):
        print(filters)
        return self.filter(
            man=filters['man'],
            woman=filters['woman'],
            name__icontains=filters['name']
        )
    