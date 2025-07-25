from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
import tempfile
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from .models import Departamento, Cargo, Empleado

# Create your views here.
def indexManagement(request):
    departamentos = Departamento.objects.all()
    cargos = Cargo.objects.all()
    return render(request, 'management/index.html', {
        'departamentos': departamentos,
        'cargos': cargos,
    })

# VISTAS DE LA SECTIONS EMPLEADOS

def generar_email(pNombre, pApellido, idempleado):
    return f'{pNombre}_{pApellido}{idempleado[-4:]}@rys.com'

def generar_codigo(pNombre, idempleado):
    nombre = (pNombre[:4] if len(pNombre) >= 4 else pNombre.ljust(4, 'X'))
    idemp = idempleado[-4:]
    return f'@{nombre}{idemp}'

def viewEmpleados(request):
    lista_empleados = Empleado.objects.all().order_by('-id')
    paginator = Paginator(lista_empleados, 15) 

    page_number = request.GET.get('page')
    empleados = paginator.get_page(page_number)
    return render(request, 'management/sections/empleados/empleados.html', {
        'empleados': empleados,
    })

def viewCrearEmpleado(request):
    departamentos = Departamento.objects.all()
    cargos = Cargo.objects.all()
    context = {
        'departamentos': departamentos,
        'cargos': cargos,
    }

    if request.method == 'POST':
        try:
            primerNombre = request.POST['primerNombre'].capitalize()
            segundoNombre = request.POST['segundoNombre'].title()
            primerApellido = request.POST['primerApellido'].capitalize()
            segundoApellido = request.POST['segundoApellido'].capitalize()
            documento = request.POST['numDocumento']

            codigo = generar_codigo(primerNombre, str(documento))
            email = generar_email(primerNombre, primerApellido, documento)

            telefono = request.POST['numTelefono']
            fechaContratacion = request.POST['fechaContratacion']
            departamento_id = request.POST['departamento']
            departamento = get_object_or_404(Departamento, id=departamento_id)
            cargo_id = request.POST['cargo']
            cargo = get_object_or_404(Cargo, id=cargo_id)
            
            empleado = Empleado.objects.create(
                primer_nombre = primerNombre,
                segundo_nombre = segundoNombre,
                primer_apellido = primerApellido,
                segundo_apellido = segundoApellido,
                documento = documento,
                codigo = codigo,
                email = email,
                telefono = telefono,
                fecha_contratacion = fechaContratacion,
                departamento = departamento,
                cargo = cargo
            )
            return redirect('vistaInfoEmpleado', empleado_id=empleado.id)
            
        except Exception as e:
            context['msg_error'] = f'Error al crear el empleado: {str(e)}'
            return render(request, 'management/sections/empleados/crear_empleado.html', context)

    return render(request, 'management/sections/empleados/crear_empleado.html', context)

def viewInfoEmpleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if request.method == 'POST':
        return redirect('vistaEliminarEmpleado', empleado_id=empleado.id)
    
    return render(request, 'management/sections/empleados/info_empleado.html', {
        'empleado': empleado,
    })

def viewEditarEmpleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    departamentos = Departamento.objects.all()
    cargos = Cargo.objects.all()
    context = {
        'empleado': empleado,
        'departamentos': departamentos,
        'cargos': cargos,
    }

    if request.method == 'POST':
        try:
            primerNombre = request.POST['primerNombre'].capitalize()
            segundoNombre = request.POST['segundoNombre'].title()
            primerApellido = request.POST['primerApellido'].capitalize()
            segundoApellido = request.POST['segundoApellido'].capitalize()
            documento = request.POST['numDocumento']
            numTelefono = request.POST['numTelefono']
            fecha_contratacion = request.POST['fechaContratacion']
            email = request.POST['email']
            codigo = request.POST['codigo']
            departamento_id = request.POST['departamento']
            departamento = get_object_or_404(Departamento, id=departamento_id)
            cargo_id = request.POST['cargo']
            cargo = get_object_or_404(Cargo, id=cargo_id)

            if len(numTelefono) != 10:
                context['msg_error'] = 'Por favor ingresa un número de telefono válido [10 digitos]'
                return render(request, 'management/sections/empleados/editar_empleado.html', context)

            if email:
                empleado.email = email
            else:
                email = generar_email(primerNombre, primerApellido, documento)
                empleado.email = email
            
            if codigo:
                empleado.codigo = codigo
            else:
                codigo = generar_codigo(primerNombre, str(documento))
                empleado.codigo = codigo

            empleado.primer_nombre = primerNombre
            empleado.segundo_nombre = segundoNombre
            empleado.primer_apellido = primerApellido
            empleado.segundo_apellido = segundoApellido
            empleado.documento = documento
            empleado.telefono = numTelefono
            empleado.fecha_contratacion = fecha_contratacion
            empleado.departamento = departamento
            empleado.cargo = cargo
            empleado.save()
            return redirect('vistaEmpleados')
        except Exception as e:
            context['msg_error'] = f'Error al editar el empleado: {str(e)}'
    return render(request, 'management/sections/empleados/editar_empleado.html', context)

def viewEliminarEmpleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('vistaEmpleados')
    return render(request, 'management/sections/empleados/eliminar_empleado.html', {
        'empleado': empleado,
    })

# VISTAS DE LA SECTIONS DEPARTAMENTOS

def viewDepartamentos(request):
    #Obtener la cantidad de empleados y cargos que tiene cada departamento
    departamentos = Departamento.objects.annotate(
        total_empleados = Count('empleado', distinct=True),
        total_cargos = Count('cargo', distinct=True)
    )

    context = {
        'departamentos': departamentos,
    }

    #CRUD en DEPARTAMENTOS
    #Crear un nuevo departamento
    if request.method == 'POST':
        if 'crearDepartamento' in request.POST:
            nombreDepartamento = request.POST.get('crearDepartamento', '').strip()
            existe = Departamento.objects.filter(nombre_departamento=nombreDepartamento).exists()
            if(existe):
                context['msg_error'] = 'Lo siento, ya existe un departamento con ese nombre. Por favor verifica tu información.'
                return render(request, 'management/sections/departamentos/departamentos.html', context)
            
            Departamento.objects.create(
                nombre_departamento=nombreDepartamento,
            )
            return redirect('vistaDepartamentos')
        #Actualizar un nuevo departamento
        elif 'actualizarDepartamento' in request.POST:
            departamento_id = request.POST['seleccionDepartamento']
            nuevo_nombre = request.POST.get('actualizarDepartamento', '').strip()
            try:
                departamento = Departamento.objects.get(id=departamento_id)
                if Departamento.objects.filter(nombre_departamento=nuevo_nombre).exclude(id=departamento.id).exists():
                    context = {
                        'departamentos': departamentos,
                        'msg_error': 'Ya existe un departamento con ese nombre'
                    }
                    return render(request, 'management/sections/departamentos/departamentos.html', context)
                departamento.nombre_departamento = nuevo_nombre
                departamento.save()
                return redirect('vistaDepartamentos')
            except Departamento.DoesNotExist:
                context = {
                    'departamentos': departamentos,
                    'msg_error': 'El departamento seleccionado no existe.'
                }
                return render(request, 'management/sections/departamentos/departamentos.html', context)
            
            except Exception as e:
                context = {
                        'departamentos': departamentos,
                        'msg_error': f'Ha ocurrido un error {str(e)}'
                    }
                return render(request, 'management/sections/departamentos/departamentos.html', context)
        #Eliminar un departamento
        elif 'selecElimDepartamento' in request.POST:
            departamento_id = request.POST['selecElimDepartamento']
            try:
                departamento = Departamento.objects.get(id=departamento_id)
                
                # Verificar si tiene empleados
                if departamento.empleado_set.exists():
                    context['msg_error'] = 'No se puede eliminar el departamento porque tiene empleados asociados'
                    return render(request, 'management/sections/departamentos/departamentos.html', context)
                    
                # Verificar si tiene cargos
                if departamento.cargo_set.exists():
                    context['msg_error'] = 'No se puede eliminar el departamento porque tiene cargos asociados'
                    return render(request, 'management/sections/departamentos/departamentos.html', context)
                    
                # Si no tiene dependencias, eliminarlo
                departamento.delete()
                return redirect('vistaDepartamentos')
                
            except Departamento.DoesNotExist:
                context['msg_error'] = 'El departamento no existe'
                return render(request, 'management/sections/departamentos/departamentos.html', context)
            except Exception as e:
                context['msg_error'] = f'Error al eliminar el departamento: {str(e)}'
                return render(request, 'management/sections/departamentos/departamentos.html', context)
            
    return render(request, 'management/sections/departamentos/departamentos.html', context)

#Función para obtener la información de cada departamento, cantidad de empleados y cargos
def obtenerInfoDepartamento(request, departamento_id):
    try:
        departamento = Departamento.objects.get(id=departamento_id)
        cargos = Cargo.objects.filter(departamento=departamento).annotate(
            total_empleados=Count('empleado') 
        )
        
        data = {
            'nombre_departamento': departamento.nombre_departamento,
            'cargos': [{
                'id': cargo.id,
                'nombre': cargo.cargo,
                'total_empleados': cargo.total_empleados
            } for cargo in cargos]
        }
        
        return JsonResponse(data)
    except Departamento.DoesNotExist:
        return JsonResponse({'error': 'Departamento no encontrado'}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)

def generarReportePDF(request, departamento_id):
    try:
        #Obtener el departamento y sus datos relacionados
        departamento = get_object_or_404(Departamento, id=departamento_id)
        
        #Obtener cargos con conteo de empleados
        cargos = Cargo.objects.filter(departamento=departamento).annotate(
            total_empleados=Count('empleado')
        )
        
        #Obtener empleados del departamento
        empleados = Empleado.objects.filter(departamento=departamento).select_related('cargo')
        
        #Calcular totales
        total_empleados = empleados.count()
        total_cargos = cargos.count()

        context = {
            'departamento': departamento,
            'cargos': cargos,
            'empleados': empleados,
            'total_empleados': total_empleados,
            'total_cargos': total_cargos
        }

        #Renderizar el template a HTML
        html_string = render_to_string('management/sections/departamentos/informe_departamento.html', context)

        #Crear la respuesta HTTP
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Informe_{departamento.nombre_departamento}_{departamento_id}.pdf"'

        #Configurar weasyprint para usar fuentes del sistema
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            response,
            presentational_hints=True
        )

        return response
        
    except Exception as e:
        print(f"Error generando PDF: {str(e)}")
        return HttpResponse(f"Error generando el PDF: {str(e)}", status=500)

# VISTAS DE LA SECTIONS CARGOS

def viewCargos(request):
    lista_cargos = Cargo.objects.annotate(
        total_empleados = Count('empleado', distinct=True)
    ).order_by('-id')

    paginator = Paginator(lista_cargos, 16) 

    page_number = request.GET.get('page')
    cargos = paginator.get_page(page_number)

    context = {
        'cargos': cargos,
    }
    return render(request, 'management/sections/cargos/cargos.html', context)

def viewCrearCargo(request):
    departamentos = Departamento.objects.all()
    context = {
        'departamentos': departamentos,
    }
    if request.method == 'POST':
        try:
            nombreCargo = request.POST['nombreCargo'].title()
            salario = request.POST['salario']
            departamento_id = request.POST['departamento']
            departamento = get_object_or_404(Departamento, id=departamento_id)
            existe = Cargo.objects.filter(cargo=nombreCargo).exists()
            if existe:
                context['msg_error'] = 'Lo siento, ese cargo ya existe, intenta con otro'
                return render(request, 'management/sections/cargos/crear_cargo.html', context)

            try:
                salario = float(salario)
            except ValueError:
                context['msg_error'] = 'Por favor ingresa un valor númerico válido para el salario'
                return render(request, 'management/sections/cargos/crear_cargo.html', context)
            
            Cargo.objects.create(
                cargo = nombreCargo,
                salario = salario,
                departamento = departamento,
            )
            return redirect('vistaCargos')
        
        except Exception as e:
            context['msg_error'] = f'Ha ocurrido un error al intentar crear el departamento {str(e)}'
            return render(request, 'management/sections/cargos/crear_cargo.html', context)
        
    return render(request, 'management/sections/cargos/crear_cargo.html', context)

def viewEditarCargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, id=cargo_id)
    departamentos = Departamento.objects.all()
    context = {
        'departamentos': departamentos,
        'cargo': cargo,
    }

    if request.method == 'POST':
        try:
            nombreCargo = request.POST['nombreCargo'].title()
            salario = request.POST['salario']
            departamento_id = request.POST['departamento']
            departamento = get_object_or_404(Departamento, id=departamento_id)

            cargo.cargo = nombreCargo
            cargo.salario = salario
            cargo.departamento = departamento
            cargo.save()
            return redirect('vistaCargos')
        except Exception as e:
            context['msg_error'] = f'Error al editar el cargo: {str(e)}'
        return render(request, 'management/sections/cargos/editar_cargo.html', context)

    return render(request, 'management/sections/cargos/editar_cargo.html', context)

def viewEliminarCargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, id=cargo_id)
    if request.method == 'POST':
        cargo.delete()
        return redirect('vistaCargos')
    return render(request, 'management/sections/cargos/eliminar_cargo.html', {
        'cargo': cargo,
    })