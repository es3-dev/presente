from django.urls import path
from . import views
urlpatterns = [
    path('', views.indexManagement, name='vistaIndexManagement'),
    path('empleados/', views.viewEmpleados, name='vistaEmpleados'),
    path('empleados/crear/', views.viewCrearEmpleado, name='vistaCrearEmpleado'),
    path('empleados/informacion_empleado/<int:empleado_id>/', views.viewInfoEmpleado, name='vistaInfoEmpleado'),
    path('empleados/editar/<int:empleado_id>', views.viewEditarEmpleado, name='vistaEditarEmpleado'),
    path('empleados/eliminar/<int:empleado_id>/', views.viewEliminarEmpleado, name='vistaEliminarEmpleado'),
    path('departamentos/', views.viewDepartamentos, name='vistaDepartamentos'),
    path('departamento/<int:departamento_id>/info/', views.obtenerInfoDepartamento, name='departamento_info'),
    path('departamento/<int:departamento_id>/reporte/', views.generarReportePDF, name='generarReporteDepartamento'),
    path('cargos/', views.viewCargos, name='vistaCargos'),
    path('cargos/crear/', views.viewCrearCargo, name='vistaCrearCargo'),
    path('cargo/editar/<int:cargo_id>', views.viewEditarCargo, name='vistaEditarCargo'),
    path('cargo/eliminar/<int:cargo_id>', views.viewEliminarCargo, name='vistaEliminarCargo'),
    path('cargo/<int:cargo_id>/reporte/', views.generarReporteCargoPDF, name='generarReporteCargo'),
]