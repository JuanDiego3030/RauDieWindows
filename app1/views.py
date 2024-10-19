from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Proyectos, Cliente, Admin
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

# Vista para index.html
def index(request):
    return render(request, 'index.html')


# Vista para el Panel de Control (solo accesible para admins)
def control(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('admin_login')  # Redirige al login si no está autenticado

    proyectos = Proyectos.objects.all()  # Obtener todos los proyectos registrados
    admin = Admin.objects.get(id=admin_id)  # Obtener información del admin autenticado
    return render(request, 'PanelDeControl.html', {'proyectos': proyectos, 'admin': admin})


# Vista para el Panel de Seguimiento (solo accesible para clientes)
def seguimiento(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('cliente_login')  # Redirige al login si no está autenticado

    cliente = Cliente.objects.get(id=cliente_id)  # Obtener información del cliente autenticado

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        requerimientos = request.POST.get('requerimientos')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado', 'Iniciado')  # Valor por defecto si no se proporciona
        fecha_inicio = request.POST.get('fecha_inicio')

        # Si no se proporciona una fecha de inicio, se usa la fecha actual
        if not fecha_inicio:
            fecha_inicio = timezone.now().date()  # Obtener solo la fecha actual

        proyecto = Proyectos(
            nombre=nombre,
            cliente=cliente.nombre,  # Guardar el nombre del cliente asociado al proyecto
            tipo=tipo,
            requerimientos=requerimientos,
            descripcion=descripcion,
            estado=estado,
            fecha_inicio=fecha_inicio  # Asegurar que tenga un valor
        )
        proyecto.save()
        return redirect('panel_seguimiento')  # Redirige al panel de seguimiento

    return render(request, 'PanelDeSeguimiento.html', {'cliente': cliente})


# Función personalizada para autenticar usuarios (admin y cliente)
def custom_authenticate(email, password, user_type):
    user = None
    if user_type == 'admin':
        try:
            admin = Admin.objects.get(email=email)
            if check_password(password, admin.password):  # Verificar la contraseña encriptada
                user = admin
        except Admin.DoesNotExist:
            pass
    elif user_type == 'cliente':
        try:
            cliente = Cliente.objects.get(email=email)
            if check_password(password, cliente.password):  # Verificar la contraseña encriptada
                user = cliente
        except Cliente.DoesNotExist:
            pass
    return user


# Vista para el login de admin
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = custom_authenticate(email=email, password=password, user_type='admin')

        if admin:
            request.session['admin_id'] = admin.id  # Guardar el ID del admin en la sesión
            return redirect('panel_control')  # Redirigir al panel de control
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'admin_login.html')

# Vista para registrar un admin
def admin_register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verificar si el correo ya está registrado
        if Admin.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado como administrador.')
        else:
            # Crear nuevo admin con contraseña encriptada
            nuevo_admin = Admin(nombre=nombre, email=email, password=make_password(password))
            nuevo_admin.save()
            request.session['admin_id'] = nuevo_admin.id  # Iniciar sesión automáticamente
            return redirect('admin_login')  # Redirigir al panel de control

    return render(request, 'admin_register.html')
    
# Vista para registrar un cliente
def cliente_register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verificar si el correo ya está registrado
        if Cliente.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado como cliente.')
        else:
            # Crear nuevo admin con contraseña encriptada
            nuevo_cliente = Cliente(nombre=nombre, email=email, password=make_password(password))
            nuevo_cliente.save()
            request.session['cliente_id'] = nuevo_cliente.id  # Iniciar sesión automáticamente
            return redirect('cliente_login')  # Redirigir al panel de control

    return render(request, 'cliente_register.html')

# Vista para el login de cliente
def cliente_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        cliente = custom_authenticate(email=email, password=password, user_type='cliente')

        if cliente:
            request.session['admin_id'] = cliente.id  # Guardar el ID del admin en la sesión
            return redirect('panel_seguimiento')  # Redirigir al panel de control
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'cliente_login.html')






# Vista para cerrar sesión
def logout(request):
    request.session.flush()  # Eliminar todas las sesiones
    return redirect('index')  # Redirigir a la página de inicio