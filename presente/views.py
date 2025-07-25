from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.conf import settings
import tempfile
from datetime import datetime
from django.core.paginator import Paginator
from .models import Reunion, Asistencia
from management.models import Departamento, Cargo

# Create your views here.
def viewIndexPresente(request):
    return render(request, 'presente/index.html', {
        'tipo_header': 'presenteCompleto',
        })

def viewCrearReunion(request):
    departamentos = Departamento.objects.all()

    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        fecha = request.POST['datetime']
        departamento_id = request.POST['departamento']
        departamento = get_object_or_404(Departamento, id=departamento_id)

        nuevaReunion = Reunion.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha=fecha,
            departamento=departamento
        )
        return redirect('vistaMostrarDetalleReunion', reunion_id=nuevaReunion.id)

    # Paginación de reuniones
    reuniones_list = Reunion.objects.all().order_by('-fecha')
    paginator = Paginator(reuniones_list, 5)  # Muestra 5 reuniones por página

    page_number = request.GET.get('page')
    reuniones = paginator.get_page(page_number)

    return render(request, 'presente/sections/reunion/reunion.html', {
        'reuniones': reuniones, 
        'departamentos': departamentos, 
        'tipo_header': 'presenteCompleto',
        })

def viewMostrarDetalleReunion(request, reunion_id):
    reunion = get_object_or_404(Reunion, id=reunion_id)
    asistencias_list = Asistencia.objects.filter(reunion=reunion)
    paginator = Paginator(asistencias_list, 5)
    page_number = request.GET.get('page')
    asistencias = paginator.get_page(page_number)
    return render(request, 'presente/sections/reunion/detalle_reunion.html', {
        'reunion': reunion, 
        'asistencias': asistencias, 
        'tipo_header': 'presenteCompleto',
        })

def viewTomarAsistencia(request, reunion_id):
    reunion = get_object_or_404(Reunion, id=reunion_id)
    if request.method == 'POST':
        nombre = request.POST['nombres']
        apellido = request.POST['apellidos']
        documento = request.POST['documento-post']
        email = request.POST['email']
        codigo = request.POST['codigo']
        cargo_id = request.POST['cargo_id'] 
        cargo = get_object_or_404(Cargo, id=cargo_id)
        #Evitar asistencias duplicadas
        registrado = Asistencia.objects.filter(documento=documento, reunion=reunion).exists()
        if registrado:
            msg_error = 'Lo siento, ya estás registrado en esta reunión.'
            return render(request, 'presente/sections/asistencia/asistencia.html', {'msg_error': msg_error})
        #En caso de que no exista, se crea el objeto en Asistencia con los datos.
        asistencia = Asistencia.objects.create(
            nombre=nombre,
            apellido=apellido,
            documento=documento,
            email=email,
            codigo=codigo,
            cargo=cargo,
            reunion=reunion
        )
        return redirect('asistenciaRegistrada')
    return render(request, 'presente/sections/asistencia/asistencia.html', {
        'reunion': reunion, 
        'tipo_header': 'presenteSimple',
        })

def asistenciaRegistrada(request):
    return render(request, 'presente/sections/asistencia/final.html', {
        'tipo_header': 'presenteSimple',
        })

def viewReportes(request):
    reuniones = Reunion.objects.all()
    return render(request, 'presente/sections/reportes/reportes.html', {
        'tipo_header': 'presenteCompleto',
        'reuniones': reuniones,
    })

def generarReportePDF(request, reunion_id):
    reunion = get_object_or_404(Reunion, id=reunion_id)
    asistencias = Asistencia.objects.filter(reunion=reunion)

    #Renderizar el template a HTML
    html_string = render_to_string('presente/sections/reportes/reporte_pdf.html', {
        'reunion': reunion,
        'asistencias': asistencias,
    })

    #Crear la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Reporte_Reunion_{reunion_id}_{reunion.titulo}_{datetime.now().strftime("%Y-%m-%d")}.pdf"'

    #Generar el PDF
    HTML(string=html_string).write_pdf(response)

    return response

# Vistas de Administración de Reuniones y Asistencias
def viewAdministracionRyA(request):
    reuniones = Reunion.objects.all().order_by('-fecha')
    asistencias = Asistencia.objects.all()
    context = {
        'reuniones': reuniones,
        'asistencias': asistencias,
        'tipo_header': 'presenteCompleto',
    }
    
    return render(request, 'presente/sections/administracion/administracion_rya.html', context)

def viewEditarReunion(request, reunion_id):
    reunion = get_object_or_404(Reunion, id=reunion_id)
    departamentos = Departamento.objects.all()
    asistencias = Asistencia.objects.filter(reunion=reunion)
    context = {
        'tipo_header': 'presenteCompleto',
        'reunion': reunion,
        'departamentos': departamentos,
        'asistencias': asistencias,
    }

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            fecha = request.POST['datetime']
            departamento_id = request.POST['departamento']
            estado = request.POST['estado']
            departamento = get_object_or_404(Departamento, id=departamento_id)

            # Actualizar la reunión
            reunion.titulo = titulo
            reunion.descripcion = descripcion
            reunion.fecha = fecha
            reunion.departamento = departamento
            reunion.estado = estado
            reunion.save()

            return redirect('vistaAdministracionRyA')
        except Exception as e:
            context['msg_error'] = f'Error al editar la reunión: {str(e)}'
            return render(request, 'presente/sections/administracion/editar_reunion.html', context)

    return render(request, 'presente/sections/administracion/editar_reunion.html', context)

def viewEliminarReunion(request, reunion_id):
    reunion = get_object_or_404(Reunion, id=reunion_id)
    
    if request.method == 'POST':
        try:
            #Condicional para verificar si hay asistencias registradas
            if Asistencia.objects.filter(reunion=reunion).exists():
                return render(request, 'presente/sections/administracion/eliminar_reunion.html', {
                    'tipo_header': 'presenteCompleto',
                    'reunion': reunion,
                    'msg_error': 'No se puede eliminar la reunión porque tiene asistencias registradas'
                })
            reunion.delete()
            return redirect('vistaAdministracionRyA')
        except Exception as e:
            return render(request, 'presente/sections/administracion/eliminar_reunion.html', {
                'tipo_header': 'presenteCompleto',
                'reunion': reunion,
                'msg_error': f'Error al eliminar la reunión: {str(e)}'
            })

    return render(request, 'presente/sections/administracion/eliminar_reunion.html', {
        'tipo_header': 'presenteCompleto',
        'reunion': reunion
    })

def viewEliminarAsistencia(request, asistencia_id):
    if request.method == 'POST':
        asistencia = get_object_or_404(Asistencia, id=asistencia_id)
        reunion_id = asistencia.reunion.id
        asistencia.delete()
        return redirect('vistaEditarReunion', reunion_id=reunion_id)
    return redirect('vistaAdministracionRyA')

