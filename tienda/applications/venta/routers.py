from rest_framework.routers import DefaultRouter

from applications.producto.viewSet import ColorViewSet,ProductViewSet
from applications.venta.viewsets import VentasViewSet

router = DefaultRouter()
router.register(r'sale', VentasViewSet, basename='sales')
urlpatterns = router.urls