from rest_framework.routers import DefaultRouter

from applications.producto.viewSet import ColorViewSet,ProductViewSet

router = DefaultRouter()
router.register(r'color', ColorViewSet, basename='color')
router.register(r'product', ProductViewSet, basename='product')
urlpatterns = router.urls