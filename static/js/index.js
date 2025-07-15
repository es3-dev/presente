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

document.addEventListener('DOMContentLoaded', () => {
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
