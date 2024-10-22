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
from django.db import models

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