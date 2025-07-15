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
# def login_personal(request):
#     return render(request, 'admin/login.html', {
#         'tipo_header': 'simple',
#     })

def indexPresente(request):
    return render(request, 'presente/index.html', {
        'tipo_header': 'presenteCompleto',
        })

def crearReunion(request):
    departamentos = Departamento.objects.all()

    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        fecha = request.POST['datetime']
        departamento_id = request.POST['departamento']
        departamento = get_object_or_404(Departamento, id=departamento_id)

        Reunion.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha=fecha,
            departamento=departamento
        )
        return redirect('reunion')

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

def mostrarDetalleReunion(request, reunion_id):
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

def tomarAsistencia(request, reunion_id):
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

    # Renderizar el template a HTML
    html_string = render_to_string('presente/sections/reportes/reporte_pdf.html', {
        'reunion': reunion,
        'asistencias': asistencias,
    })

    # Crear la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_reunion_{reunion_id}_{datetime.now().strftime("%Y%m%d")}.pdf"'

    # Generar el PDF
    HTML(string=html_string).write_pdf(response)

    return response