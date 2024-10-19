from django.shortcuts import render, redirect, get_object_or_404
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
    admin = get_object_or_404(Admin, id=admin_id)  # Obtener información del admin autenticado

    if request.method == 'POST':
        if 'eliminar_proyecto' in request.POST:
            proyecto_id = request.POST.get('proyecto_id')
            proyecto = get_object_or_404(Proyectos, id=proyecto_id)
            proyecto.delete()
            messages.success(request, 'Proyecto eliminado correctamente.')
            return redirect('panel_control')

        if 'cambiar_estatus' in request.POST:
            proyecto_id = request.POST.get('proyecto_id')
            nuevo_estatus = request.POST.get('estado')

            if not nuevo_estatus:  # Verificar que el nuevo estado no esté vacío
                messages.error(request, 'Por favor, selecciona un estado válido.')
                return redirect('panel_control')

            proyecto = get_object_or_404(Proyectos, id=proyecto_id)
            proyecto.estado = nuevo_estatus
            proyecto.save()
            messages.success(request, 'Estatus del proyecto actualizado.')
            return redirect('panel_control')

    return render(request, 'PanelDeControl.html', {'proyectos': proyectos, 'admin': admin})


# Vista para el Panel de Seguimiento (solo accesible para clientes)
def seguimiento(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('cliente_login')  # Redirige al login si no está autenticado

    cliente = get_object_or_404(Cliente, id=cliente_id)  # Obtener información del cliente autenticado
    proyectos = Proyectos.objects.filter(cliente=cliente)  # Filtrar proyectos del cliente
    
    # Contexto inicial con nombre del cliente
    context = {
        'cliente': cliente,
        'proyectos': proyectos,
        'nombre_cliente': cliente.nombre,  # Asumiendo que el modelo Cliente tiene un campo nombre
    }

    if request.method == 'POST':
        proyecto_id = request.POST.get('proyecto_id')

        # Si el proyecto ya existe, actualízalo
        if proyecto_id:
            proyecto = get_object_or_404(Proyectos, id=proyecto_id)
            proyecto.tipo = request.POST.get('tipo', proyecto.tipo)
            proyecto.requerimientos = request.POST.get('requerimientos', proyecto.requerimientos)
            proyecto.descripcion = request.POST.get('descripcion', proyecto.descripcion)
            proyecto.estado = request.POST.get('estado', proyecto.estado)
            proyecto.fecha_inicio = request.POST.get('fecha_inicio', proyecto.fecha_inicio)
            proyecto.save()
            messages.success(request, 'Proyecto actualizado con éxito')

        # Si no hay proyecto_id, crea un nuevo proyecto
        else:
            nombre = request.POST.get('nombre')  # Obtener el nombre del proyecto
            tipo = request.POST.get('tipo')
            requerimientos = request.POST.get('requerimientos')
            descripcion = request.POST.get('descripcion')
            estado = request.POST.get('estado', 'Planeando')  # Establecer estado por defecto
            fecha_inicio = request.POST.get('fecha_inicio', timezone.now())  # Usa la fecha actual si no se proporciona

            nuevo_proyecto = Proyectos(
                cliente=cliente,
                nombre=nombre,  # Asignar el nombre del proyecto
                tipo=tipo,
                requerimientos=requerimientos,
                descripcion=descripcion,
                estado=estado,
                fecha_inicio=fecha_inicio,
            )
            nuevo_proyecto.save()
            messages.success(request, 'Proyecto creado con éxito')

        return redirect('panel_seguimiento')  # Redirige al panel de seguimiento

    return render(request, 'PanelDeSeguimiento.html', context)  # Renderiza con el contexto actualizado

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
            request.session['cliente_id'] = cliente.id  # Guardar el ID del cliente en la sesión
            return redirect('panel_seguimiento')  # Redirigir al panel de seguimiento
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'cliente_login.html')



# Vista para cerrar sesión
def logout(request):
    request.session.flush()  # Eliminar todas las sesiones
    return redirect('index')  # Redirigir a la página de inicio