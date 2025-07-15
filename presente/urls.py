from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.login_personal, name='login'),
    path('', views.indexPresente, name='indexPresente'),
    path('reunion/', views.crearReunion, name='reunion'),
    path('reunion/<int:reunion_id>/detalle/', views.mostrarDetalleReunion, name='mostrarDetalleReunion'),
    path('reunion/<int:reunion_id>/asistencia/', views.tomarAsistencia, name='tomarAsistencia'),
    path('reunion/registro_exitoso/', views.asistenciaRegistrada, name='asistenciaRegistrada'),
    path('reportes/', views.viewReportes, name='vistaReportes'),
    path('reunion/<int:reunion_id>/reporte/', views.generarReportePDF, name='generar_reporte_pdf'),
]