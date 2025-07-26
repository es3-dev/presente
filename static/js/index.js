// Funcionar para copiar enlace de reunion
function copy_link() {
    const input = document.getElementById('enlace');
    const btn = document.getElementById('btn-copy-link');

    navigator.clipboard.writeText(input.value)
        .then(() => {
            const originalText = btn.textContent;
            btn.textContent = '¡Copiado!';
            btn.disabled = true;

            setTimeout(() => {
                btn.textContent = originalText;
                btn.disabled = false;
            }, 2000);
        })
        .catch(err => {
            console.error('Error al copiar:', err);
            alert('No se pudo copiar el enlace');
        });
}


function buscarReuniones() {
    const searchTerm = document.getElementById('search-reuniones').value.toLowerCase();
    const rows = document.querySelectorAll('#tab-reuniones tbody tr');
            
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

function buscarAsistenciasEnTabla() {
    const searchTerm = document.getElementById('search-asistencias').value.toLowerCase();
    const tabla = document.querySelector('table');
    if (!tabla) return;

    const rows = tabla.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

// Función para buscar empleados
function buscarEmpleados() {
    const searchInput = document.getElementById('search-empleados');
    const searchTerm = searchInput.value.toLowerCase();
    const rows = document.querySelectorAll('tbody tr');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}


document.addEventListener('DOMContentLoaded', () => {
    // Configurar el menú móvil
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            mobileMenu.classList.toggle('flex');
            mobileMenu.classList.toggle('flex-col');
        });
    }

    // Configurar el menú móvil de management
    const mobileMenuButtonManagement = document.getElementById('mobile-menu-button-management');
    const mobileMenuManagement = document.getElementById('mobile-menu-management');

    if (mobileMenuButtonManagement && mobileMenuManagement) {
        mobileMenuButtonManagement.addEventListener('click', () => {
            mobileMenuManagement.classList.toggle('hidden');
            mobileMenuManagement.classList.toggle('flex');
            mobileMenuManagement.classList.toggle('flex-col');
        });
    }

    // Configurar búsqueda de cargos
    const searchCargos = document.getElementById('search-cargos');
    if (searchCargos) {
        searchCargos.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const cards = document.querySelectorAll('[data-cargo]');

            cards.forEach(card => {
                const cargoText = card.getAttribute('data-cargo').toLowerCase();
                const contenidoCard = card.textContent.toLowerCase();
                
                // Busca tanto en el nombre del cargo como en todo el contenido de la tarjeta
                const coincide = cargoText.includes(searchTerm) || contenidoCard.includes(searchTerm);
                card.style.display = coincide ? '' : 'none';
            });
        });
    }

    //Función para buscar reuniones en la section de Reportes
    const inputBusqueda = document.getElementById('busqueda');
    if(inputBusqueda){
        const cards = document.querySelectorAll('[data-titulo]');

        inputBusqueda.addEventListener('input', function(e){
        const terminoBusqueda = e.target.value.toLowerCase().trim();

        cards.forEach(card =>{
            const titulo = card.dataset.titulo;
            const descripcion = card.dataset.descripcion;
            const fecha = card.dataset.fecha;

            const coincide = titulo.includes(terminoBusqueda) || descripcion.includes(terminoBusqueda) || fecha.includes(terminoBusqueda);

            card.style.display = coincide ? 'flex' : 'none'
        });

    });
    }
    
    // Seleccionar todos los enlaces "Ver información completa"
    const enlaces = document.querySelectorAll('.ver-info-departamento');
    
    enlaces.forEach(enlace => {
        enlace.addEventListener('click', function(e) {
            e.preventDefault();
            const departamentoId = this.getAttribute('data-departamento-id');
            
            // Hacer la petición AJAX
            fetch(`/management/departamento/${departamentoId}/info/`)
                .then(response => response.json())
                .then(data => {
                    // Actualizar el contenido del aside
                    document.querySelector('#nombreDepartamento').textContent = data.nombre_departamento;
                    
                    // Actualizar el botón de reporte
                    const btnReporte = document.querySelector('#btnReporte');
                    btnReporte.style.display = 'block';
                    btnReporte.href = `/management/departamento/${departamentoId}/reporte/`;
                    
                    // Actualizar la tabla de cargos
                    const tablaCargos = document.querySelector('#tablaCargos tbody');
                    tablaCargos.innerHTML = ''; // Limpiar tabla actual
                    
                    data.cargos.forEach((cargo, index) => {
                        tablaCargos.innerHTML += `
                            <tr class="border-t border-gray-200 hover:bg-gray-50 transition">
                                <td class="px-3 py-2 text-center text-sm">${index + 1}</td>
                                <td class="px-3 py-2 text-center text-sm">${cargo.nombre}</td>
                                <td class="px-2 py-1 text-center text-sm">${cargo.total_empleados}</td>
                            </tr>
                        `;
                    });
                });
        });
    });


    const btnCancelar = document.getElementById('btnCancelarAccion');
    if (btnCancelar) {
        btnCancelar.addEventListener('click', function(e) { 
            e.preventDefault();
            const inputEdicionDepartamento = document.getElementById('actualizarDepartamento');
            if (inputEdicionDepartamento) {
                inputEdicionDepartamento.value = '';
            }
        });
    }

    const btnConsultar = document.getElementById('btn-consultar')
    if (btnConsultar){
        btnConsultar.addEventListener('click', function (e) {
        e.preventDefault();
        const documento = document.getElementById('documento').value;
        if (!documento) {
            alert('Por favor ingresa un número de documento.');
            return;
        }

        fetch(`/api/empleado/${documento}/`)
            .then(response => {
                if (!response.ok) throw new Error('No encontrado');
                return response.json();
            })
            .then(data => {
                document.getElementById('nombres').value = `${data.primer_nombre} ${data.segundo_nombre}` || '';
                document.getElementById('apellidos').value = `${data.primer_apellido} ${data.segundo_apellido}` || '';
                document.getElementById('documento-post').value = data.documento || '';
                document.getElementById('codigo').value = data.codigo || '';
                document.getElementById('email').value = data.email || '';
                document.getElementById('cargo').value = data.cargo.cargo || '';
                document.getElementById('cargo_id').value = data.cargo.id || '';
                document.getElementById('btn-confirmar').hidden = false;
            })
            .catch(() => {
                alert('Empleado no encontrado.');
                ['nombres', 'apellidos', 'codigo', 'email', 'cargo']
                    .forEach(id => document.getElementById(id).value = '');
                document.getElementById('btn-confirmar').hidden = true;
            });
    });
    }
});
