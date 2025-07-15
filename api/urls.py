from rest_framework.routers import DefaultRouter
from .views import EmpleadoViewSet, ReunionViewSet

router = DefaultRouter()
router.register(r'empleado', EmpleadoViewSet, basename='empleado')
router.register(r'reunion', ReunionViewSet, basename='reunion')


urlpatterns = router.urls