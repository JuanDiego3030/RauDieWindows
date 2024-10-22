// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // Obtener el formulario
    const form = document.querySelector('form');

    if (form) {
        // Añadir el evento submit al formulario
        form.addEventListener('submit', function(event) {
            // Obtener valores de los campos
            const projectName = document.getElementById('projectName') ? document.getElementById('projectName').value.trim() : "";
            const projectType = document.getElementById('projectType') ? document.getElementById('projectType').value : "";
            const projectDescription = document.getElementById('projectDescription') ? document.getElementById('projectDescription').value.trim() : "";
            const projectRequirements = document.getElementById('projectRequirements') ? document.getElementById('projectRequirements').value.trim() : "";

            // Verificar si algún campo está vacío
            if (!projectName || projectType === "Selecciona el tipo de proyecto" || !projectDescription || !projectRequirements) {
                alert("Por favor, completa todos los campos antes de enviar.");
                event.preventDefault(); // Evitar el envío del formulario
            }
        });
    }

    // Manejar el modal de modificación de proyectos si existe en la página
    const modifyProjectModal = document.getElementById('modifyProjectModal');
    if (modifyProjectModal) {
        modifyProjectModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget; // Botón que disparó el modal
            const projectId = button.getAttribute('data-proyecto-id');
            const projectName = button.getAttribute('data-nombre');
            const projectType = button.getAttribute('data-tipo');
            const projectDescription = button.getAttribute('data-descripcion');
            const projectRequirements = button.getAttribute('data-requerimientos');

            // Rellenar el formulario del modal con los datos del proyecto
            document.getElementById('modifyProjectId').value = projectId;
            document.getElementById('modifyProjectName').value = projectName;
            document.getElementById('modifyProjectType').value = projectType;
            document.getElementById('modifyProjectDescription').value = projectDescription;
            document.getElementById('modifyProjectRequirements').value = projectRequirements;
        });
    }
});
