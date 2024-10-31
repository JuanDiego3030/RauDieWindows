from django.utils import timezone
from django.db import models

# modelo Admins
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

# Nueva tabla para Etapa en proyectos
class Etapa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, related_name="etapas")

    def __str__(self):
        return f"{self.nombre} - {self.proyecto.nombre}"

# Nueva tabla para Comentarios en proyectos
class Comentario(models.Model):
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, related_name="comentarios", null=True, blank=True)
    autor = models.CharField(max_length=100)  # Agregar campo autor

    def __str__(self):
        return f"Comentario de {self.autor} sobre {self.proyecto.nombre}"
    
# Modelo de administración para gestión de usuarios
class Admin_user(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del usuario admin
    email = models.EmailField(max_length=255, unique=True)  # Correo del usuario admin
    password = models.CharField(max_length=255)  # Contraseña del usuario admin
 # Estado activo o inactivo del usuario admin

    def __str__(self):
        return f"Admin User: {self.nombre}"

# Modelo para bloquear usuarios (Clientes y Admins)
class User_block(models.Model):
    usuario_id = models.IntegerField()  # ID del usuario bloqueado
    es_cliente = models.BooleanField()  # True si es un cliente, False si es admin
    fecha_bloqueo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        tipo_usuario = "Cliente" if self.es_cliente else "Admin"
        return f"{tipo_usuario} bloqueado ID: {self.usuario_id}"

