from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.login_personal, name='login'),
    path('presente/', views.viewIndexPresente, name='vistaIndexPresente'),
    path('reunion/', views.viewCrearReunion, name='vistaCrearReunion'),
    path('reunion/<int:reunion_id>/detalle/', views.viewMostrarDetalleReunion, name='vistaMostrarDetalleReunion'),
    path('reunion/<int:reunion_id>/asistencia/', views.viewTomarAsistencia, name='tomarAsistencia'),
    path('reunion/registro_exitoso/', views.asistenciaRegistrada, name='asistenciaRegistrada'),
    path('reportes/', views.viewReportes, name='vistaReportes'),
    path('reunion/<int:reunion_id>/reporte/', views.generarReportePDF, name='generar_reporte_pdf'),
    path('administracion/', views.viewAdministracionRyA, name='vistaAdministracionRyA'),
    path('administracion/reunion/editar/<int:reunion_id>/', views.viewEditarReunion, name='vistaEditarReunion'),
    path('administracion/reunion/eliminar/<int:reunion_id>/', views.viewEliminarReunion, name='vistaEliminarReunion'),
    path('administracion/asistencia/eliminar/<int:asistencia_id>/', views.viewEliminarAsistencia, name='vistaEliminarAsistencia'),
]