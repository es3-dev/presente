from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Departamento, Cargo, Empleado

# Create your views here.
def indexManagement(request):
    departamentos = Departamento.objects.all()
    cargos = Cargo.objects.all()
    if request.method == 'POST':
        primerNombre = request.POST['primerNombre']
        segundoNombre = request.POST['segundoNombre']
        primerApellido = request.POST['primerApellido']
        segundoApellido = request.POST['segundoApellido']
        documento = int(request.POST['documento'])

        def generar_codigo(pNombre, idempleado):
            nombre = (pNombre[:4] if len(pNombre) >= 4 else pNombre.ljust(4, 'X'))
            idemp = idempleado[-4:]
            return f'@{nombre}{idemp}'
        codigo = generar_codigo(primerNombre, str(documento))

        email = request.POST['email']
        telefono = int(request.POST['telefono'])
        fechaContratacion = request.POST['fecha_contratacion']
        departamento_id = request.POST['departamento_id']
        departamento = get_object_or_404(Departamento, id=departamento_id)
        cargo_id = request.POST['cargo_id']
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
        empleado.save()
        return redirect('index-management')
    return render(request, 'management/index.html', {
        'departamentos': departamentos,
        'cargos': cargos,
    })

def viewEmpleados(request):
    lista_empleados = Empleado.objects.all().order_by('-id')
    paginator = Paginator(lista_empleados, 15) 

    page_number = request.GET.get('page')
    empleados = paginator.get_page(page_number)
    return render(request, 'management/sections/empleados/empleados.html', {
        'empleados': empleados,

    })

def viewInfoEmpleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    return render(request, 'management/sections/empleados/informacion_empleado.html', {
        'empleado': empleado,
    })

def viewDepartamentos(request):
    departamentos = Departamento.objects.all()
    if request.method == 'POST':
        nombreDepartamento = request.POST['nombreDepartamento']
        existe = Departamento.objects.filter(nombre_departamento=nombreDepartamento).exists()
        if(existe):
            msg_error = 'Lo siento, ya existe un departamento con ese nombre. Por favor verifica tu información.'
            return render(request, 'management/sections/departamentos/departamentos.html')
        Departamento.objects.create(
            nombre_departamento=nombreDepartamento,
        )
        return redirect('vistaDepartamentos')
    return render(request, 'management/sections/departamentos/departamentos.html', {
        'departamentos': departamentos,
    })

def viewCargos(request):
    cargos = Cargo.objects.all()
    if request.method == 'POST':
        cargo = request.POST['cargo']
        salario = request.POST['salario']
        departamento_id = request.POST['departamento']
        departamento = get_object_or_404(Departamento, id=departamento_id)
        existe = Cargo.objects.filter(cargo=cargo).exists()
        if existe:
            msg_error = 'Lo siento, ya existe un cargo con ese nombre. Por favor verifica tu información.'
            return render(request, 'management/sections/cargos/cargos.html', {
                'msg_error': msg_error,
            })
        Cargo.objects.create(
            cargo=cargo,
            salario=salario,
            departamento=departamento,
        )
        return redirect('vistaCargos')
    return render(request, 'management/sections/cargos/cargos.html', {
        'cargos': cargos,
    })
