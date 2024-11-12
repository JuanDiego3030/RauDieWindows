from django.contrib.auth.hashers import make_password
from app1.models import Admin_user  # Cambia 'app1' por el nombre de tu aplicación

# Datos de los administradores a agregar
admin_data = [
    {"nombre": "Juan Arana", "email": "juanarana@gmail.com", "password": "12345678"},
    {"nombre": "Martin Hermoso", "email": "martinhermoso@gmail.com", "password": "12345678"},
    {"nombre": "Jose De Sousa", "email": "josedesousa@gmail.com", "password": "12345678"},
    {"nombre": "Raulymar De Abreu", "email": "raulymardea@gmail.com", "password": "12345678"},
    {"nombre": "Jackson Perez", "email": "jacksonperez@gmail.com", "password": "30463584"},
]

# Crear instancias de Admin_user y guardarlas en la base de datos
for admin in admin_data:
    Admin_user.objects.create(
        nombre=admin["nombre"],
        email=admin["email"],
        password=make_password(admin["password"]),
    )

print("Datos de los administradores agregados con éxito.")

