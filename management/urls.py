from django.urls import path
from . import views
urlpatterns = [
    path('', views.indexManagement, name='vistaIndexManagement'),
    path('departamentos/', views.viewDepartamentos, name='vistaDepartamentos'),
    path('cargos/', views.viewCargos, name='vistaCargos'),
    path('empleados/', views.viewEmpleados, name='vistaEmpleados'),
    path('informacion/<int:empleado_id>/', views.viewInfoEmpleado, name='vistaInfoEmpleado'),
    path('departamento/<int:departamento_id>/info/', views.obtenerInforDepartamento, name='departamento_info'),
    path('departamento/<int:departamento_id>/reporte/', views.generarReportePDF, name='generarReporteDepartamento')
]