from django.utils import timezone
from django.db import models

# Custom model for Admins
class Admin(models.Model):
    nombre = models.CharField(max_length=100)  # Agregado campo de nombre
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

# Custom model for Clients
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)  # Agregado campo de nombre
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

# Modelo para los proyectos
class Proyectos(models.Model):
    nombre = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con Cliente
    tipo = models.CharField(max_length=100)
    requerimientos = models.TextField()
    descripcion = models.TextField()
    estado = models.CharField(max_length=50, default='Planeando')
    fecha_inicio = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nombre

#Modelo para las tares
class Tarea(models.Model):
    ESTADOS = [
        ('Completada', 'Completada'),
        ('En progreso', 'En progreso'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    def __str__(self):
        return self.nombre

# Nueva tabla para Etapa en proyectos o tareas
class Etapa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, related_name="etapas")

    def __str__(self):
        return f"{self.nombre} - {self.proyecto.nombre}"

# Nueva tabla para Comentarios en proyectos o tareas
class Comentario(models.Model):
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, related_name="comentarios", null=True, blank=True)
    autor = models.CharField(max_length=100)  # Agregar campo autor

    def __str__(self):
        return f"Comentario de {self.autor} sobre {self.proyecto.nombre}"

# Nueva tabla para Documentos asociados a proyectos o tareas
class Documento(models.Model):
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='documentos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, related_name="documentos", null=True, blank=True)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="documentos", null=True, blank=True)

    def __str__(self):
        return self.titulo

# Nueva tabla para Asignaciones de tareas a clientes o admins
class Asignacion(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="asignaciones")
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asignación de {self.tarea.nombre}"
