from django.urls import path
from . import views
urlpatterns = [
    path('', views.indexManagement, name='vistaIndexManagement'),
    path('departamentos/', views.viewDepartamentos, name='vistaDepartamentos'),
    path('departamento/<int:departamento_id>/info/', views.obtenerInforDepartamento, name='departamento_info'),
    path('departamento/<int:departamento_id>/reporte/', views.generarReportePDF, name='generarReporteDepartamento'),
    path('cargos/', views.viewCargos, name='vistaCargos'),
    path('empleados/', views.viewEmpleados, name='vistaEmpleados'),
    path('empleados/crear/', views.viewCrearEmpleado, name='vistaCrearEmpleado'),
    path('empleados/informacion_empleado/<int:empleado_id>/', views.viewInfoEmpleado, name='vistaInfoEmpleado'),
    path('empleados/editar/<int:empleado_id>', views.viewEditarEmpleado, name='vistaEditarEmpleado'),
    path('empleados/eliminar/<int:empleado_id>/', views.viewEliminarEmpleado, name='vistaEliminarEmpleado'),
]