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

# Modelo para los proyectos (sin cambios)
class Proyectos(models.Model):
    nombre = models.CharField(max_length=200)
    cliente = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    requerimientos = models.TextField()
    descripcion = models.TextField()
    estado = models.CharField(max_length=50, default='Planeando')
    fecha_inicio = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nombre

