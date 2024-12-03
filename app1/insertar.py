from django.contrib.auth.hashers import make_password
from app1.models import Admin_user 

# Datos de los administradores a agregar
admin_data = [
    {"nombre": "Juan Arana", "email": "juanarana@gmail.com", "password": "12345678"},
]

# Crear instancias y guardarlas en la base de datos
for admin in admin_data:
    Admin_user.objects.create(
        nombre=admin["nombre"],
        email=admin["email"],
        password=make_password(admin["password"]),
    )

print("Datos de los administradores agregados con éxito.")

