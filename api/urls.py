from rest_framework.routers import DefaultRouter
from .views import EmpleadoViewSet, DepartamentoViewSet, CargoViewSet, ReunionViewSet, AsistenciaViewSet

router = DefaultRouter()
router.register(r'empleado', EmpleadoViewSet, basename='empleado')
router.register(r'departamento', DepartamentoViewSet, basename='departamento')
router.register(r'cargo', CargoViewSet, basename='cargo')
router.register(r'reunion', ReunionViewSet, basename='reunion')
router.register(r'asistencia', AsistenciaViewSet, basename='asistencia')


urlpatterns = router.urls