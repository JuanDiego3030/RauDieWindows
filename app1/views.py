from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Proyectos, Cliente, Admin, Tarea, Etapa, Comentario, User_block, Admin_user
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail

# Vista para index.html
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        print(f"Nombre: {name}, Email: {email}, Asunto: {subject}, Mensaje: {message}")  # Para depurar
        
        # Enviar correo
        try:
            send_mail(
                subject,
                f'Mensaje de {name} <{email}>:\n\n{message}',
                'juanxcosa@gmail.com',  # Cambia esto por tu correo
                ['juandiegoaranaperez@gmail.com'],  # Cambia esto por el correo del destinatario
                fail_silently=False,
            )
            messages.success(request, 'Mensaje enviado con éxito.')
            return redirect('index')  # Redirige a la vista de índice
        except Exception as e:
            print(e)  # Imprimir el error para depurar
            messages.error(request, 'Hubo un error al enviar tu mensaje. Inténtalo de nuevo.')

    return render(request, 'index.html')

# Vista para el Panel de Control (solo accesible para admins)
def control(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('admin_login')  # Redirige al login si no está autenticado

    proyectos = Proyectos.objects.all()  # Obtener todos los proyectos registrados
    admin = get_object_or_404(Admin, id=admin_id)  # Obtener información del admin autenticado
    tareas = Tarea.objects.all()  # Obtener todas las tareas registradas
    etapas = Etapa.objects.all()  # Obtener todas las etapas registradas

    if request.method == 'POST':
        # Lógica para eliminar y actualizar proyectos y tareas
        if 'eliminar_proyecto' in request.POST:
            proyecto_id = request.POST.get('proyecto_id')
            proyecto = get_object_or_404(Proyectos, id=proyecto_id)
            proyecto.delete()
            messages.success(request, 'Proyecto eliminado correctamente.')
            return redirect('panel_control')

        if 'cambiar_estatus' in request.POST:
            proyecto_id = request.POST.get('proyecto_id')
            nuevo_estatus = request.POST.get('estado')
            proyecto = get_object_or_404(Proyectos, id=proyecto_id)
            proyecto.estado = nuevo_estatus
            proyecto.save()
            messages.success(request, 'Estatus del proyecto actualizado.')
            return redirect('panel_control')
        
        if 'agregar_tarea' in request.POST:
            nombre = request.POST.get('nombre_tarea')
            descripcion = request.POST.get('descripcion_tarea')
            estado = request.POST.get('estado_tarea')
            nueva_tarea = Tarea(nombre=nombre, descripcion=descripcion, estado=estado)
            nueva_tarea.save()
            messages.success(request, 'Tarea añadida correctamente.')
            return redirect('panel_control')

        if 'eliminar_tarea' in request.POST:
            tarea_id = request.POST.get('tarea_id')
            tarea = get_object_or_404(Tarea, id=tarea_id)
            tarea.delete()
            messages.success(request, 'Tarea eliminada correctamente.')
            return redirect('panel_control')
        
        
        if 'cambiar_estatus_tarea' in request.POST:
            tarea_id = request.POST.get('tarea_id')
            nuevo_estado = request.POST.get('estado_tarea')
            tarea = get_object_or_404(Tarea, id=tarea_id)
            tarea.estado = nuevo_estado
            tarea.save()
            messages.success(request, f'Estatus de la tarea actualizado a "{nuevo_estado}".')
            return redirect('panel_control')

        # Nueva lógica para agregar, actualizar y eliminar etapas
        if 'agregar_etapa' in request.POST:
            nombre = request.POST.get('nombre_etapa')
            descripcion = request.POST.get('descripcion_etapa')
            proyecto_id = request.POST.get('proyecto_id')
            proyecto = get_object_or_404(Proyectos, id=proyecto_id)
            nueva_etapa = Etapa(nombre=nombre, descripcion=descripcion, proyecto=proyecto)
            nueva_etapa.save()
            messages.success(request, 'Etapa añadida correctamente.')
            return redirect('panel_control')

        if 'eliminar_etapa' in request.POST:
            etapa_id = request.POST.get('etapa_id')
            etapa = get_object_or_404(Etapa, id=etapa_id)
            etapa.delete()
            messages.success(request, 'Etapa eliminada correctamente.')
            return redirect('panel_control')

        if 'actualizar_etapa' in request.POST:
            etapa_id = request.POST.get('etapa_id')
            nombre = request.POST.get('nombre_etapa')
            descripcion = request.POST.get('descripcion_etapa')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            
            # Validaciones de campos
            if not nombre or not descripcion:
                messages.error(request, 'El nombre y la descripción son obligatorios.')
                return redirect('panel_control')
            if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
                messages.error(request, 'La fecha de inicio no puede ser posterior a la fecha de fin.')
                return redirect('panel_control')
            
            # Actualización de la etapa
            etapa = get_object_or_404(Etapa, id=etapa_id)
            etapa.nombre = nombre
            etapa.descripcion = descripcion
            etapa.fecha_inicio = fecha_inicio or etapa.fecha_inicio
            etapa.fecha_fin = fecha_fin
            etapa.save()
            messages.success(request, 'Etapa actualizada correctamente.')
            return redirect('panel_control')

    return render(request, 'PanelDeControl.html', {'proyectos': proyectos, 'admin': admin, 'tareas': tareas, 'etapas': etapas})

# Vista para el Panel de Seguimiento (solo accesible para clientes)
def seguimiento(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('cliente_login')  # Redirige al login si no está autenticado

    cliente = get_object_or_404(Cliente, id=cliente_id)
    proyectos = Proyectos.objects.filter(cliente=cliente)

    # Añadir comentarios en el contexto
    comentarios_por_proyecto = {proyecto.id: proyecto.comentarios.all() for proyecto in proyectos}

    context = {
        'cliente': cliente,
        'proyectos': proyectos,
        'comentarios_por_proyecto': comentarios_por_proyecto,
        'nombre_cliente': cliente.nombre,
    }

    if request.method == 'POST':
        proyecto_id = request.POST.get('proyecto_id')

        if 'comentario' in request.POST:
            # Manejo de adición de comentario
            contenido_comentario = request.POST.get('comentario')
            if proyecto_id:
                proyecto = get_object_or_404(Proyectos, id=proyecto_id)
                comentario = Comentario.objects.create(
                    contenido=contenido_comentario,
                    proyecto=proyecto,
                    autor=cliente.nombre  # Asigna el nombre del cliente como autor
                )
                messages.success(request, 'Comentario agregado con éxito')
            else:
                messages.error(request, 'Por favor, selecciona un proyecto para comentar')

        elif 'eliminar_comentario' in request.POST:
            # Manejo de eliminación de comentario
            comentario_id = request.POST.get('comentario_id')
            comentario = get_object_or_404(Comentario, id=comentario_id)
            comentario.delete()
            messages.success(request, 'Comentario eliminado con éxito')

        else:
            # Lógica para actualizar o crear proyectos
            if proyecto_id:
                proyecto = get_object_or_404(Proyectos, id=proyecto_id)
                proyecto.tipo = request.POST.get('tipo', proyecto.tipo)
                proyecto.requerimientos = request.POST.get('requerimientos', proyecto.requerimientos)
                proyecto.descripcion = request.POST.get('descripcion', proyecto.descripcion)
                proyecto.estado = request.POST.get('estado', proyecto.estado)
                proyecto.fecha_inicio = request.POST.get('fecha_inicio', proyecto.fecha_inicio)
                proyecto.save()
                messages.success(request, 'Proyecto actualizado con éxito')
            else:
                nombre = request.POST.get('nombre')
                tipo = request.POST.get('tipo')
                requerimientos = request.POST.get('requerimientos')
                descripcion = request.POST.get('descripcion')
                estado = request.POST.get('estado', 'Planeando')
                fecha_inicio = request.POST.get('fecha_inicio', timezone.now())

                nuevo_proyecto = Proyectos.objects.create(
                    cliente=cliente,
                    nombre=nombre,
                    tipo=tipo,
                    requerimientos=requerimientos,
                    descripcion=descripcion,
                    estado=estado,
                    fecha_inicio=fecha_inicio,
                )
                messages.success(request, 'Proyecto creado con éxito')

        return redirect('panel_seguimiento')  # Redirige al panel de seguimiento

    return render(request, 'PanelDeSeguimiento.html', context)

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
        
        # Verificar si el usuario está bloqueado
        admin = Admin.objects.filter(email=email).first()
        if admin and User_block.objects.filter(usuario_id=admin.id, es_cliente=False).exists():
            messages.error(request, 'Este usuario está bloqueado.')
            return render(request, 'admin_login.html')

        # Autenticar al usuario si no está bloqueado
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

        # Verificar si la contraseña tiene al menos 8 caracteres
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'admin_register.html')

        # Verificar si el correo ya está registrado
        if Admin.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado como administrador.')
        else:
            # Crear nuevo admin con contraseña encriptada
            nuevo_admin = Admin(nombre=nombre, email=email, password=make_password(password))
            nuevo_admin.save()
            request.session['admin_id'] = nuevo_admin.id  # Iniciar sesión automáticamente
            messages.success(request, 'Administrador agregado con éxito')
            return redirect('admin_login')  # Redirigir al panel de control

    return render(request, 'admin_register.html')

# Vista para registrar un cliente
def cliente_register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verificar si la contraseña tiene al menos 8 caracteres
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'cliente_register.html')

        # Verificar si el correo ya está registrado
        if Cliente.objects.filter(email=email).exists():
            messages.error(request, 'Este correo ya está registrado como cliente.')
        else:
            # Crear nuevo cliente con contraseña encriptada
            nuevo_cliente = Cliente(nombre=nombre, email=email, password=make_password(password))
            nuevo_cliente.save()
            request.session['cliente_id'] = nuevo_cliente.id  # Iniciar sesión automáticamente
            messages.success(request, 'Cliente agregado con éxito')
            return redirect('cliente_login')  # Redirigir al panel de control
        
    return render(request, 'cliente_register.html')

# Vista para el login de cliente
def cliente_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Verificar si el cliente está bloqueado
        cliente = Cliente.objects.filter(email=email).first()
        if cliente and User_block.objects.filter(usuario_id=cliente.id, es_cliente=True).exists():
            messages.error(request, 'Este usuario está bloqueado.')
            return render(request, 'cliente_login.html')

        # Autenticar al cliente si no está bloqueado
        cliente = custom_authenticate(email=email, password=password, user_type='cliente')
        if cliente:
            request.session['cliente_id'] = cliente.id  # Guardar el ID del cliente en la sesión
            return redirect('panel_seguimiento')  # Redirigir al panel de seguimiento
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'cliente_login.html')

# Vista para gestionar usuarios
def gestionar_usuarios(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('gestion_login')  # Redirige al login si no está autenticado

    # Obtén todos los clientes y administradores
    clientes = Cliente.objects.all()
    admins = Admin.objects.all()
    bloqueados = User_block.objects.all()  # Obtener todos los usuarios bloqueados

    # Manejo de peticiones POST
    if request.method == 'POST':
        # Edición de clientes
        if 'modificar_cliente' in request.POST:
            cliente_id = request.POST.get('cliente_id')
            nombre = request.POST.get('nombre')
            email = request.POST.get('email')
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                cliente.nombre = nombre
                cliente.email = email
                cliente.save()
                messages.success(request, 'Cliente editado con éxito.')
            except Cliente.DoesNotExist:
                messages.error(request, 'Cliente no encontrado.')

        # Edición de administradores
        elif 'modificar_admin' in request.POST:
            admin_id = request.POST.get('admin_id')
            nombre = request.POST.get('nombre')
            email = request.POST.get('email')
            try:
                admin = Admin.objects.get(id=admin_id)
                admin.nombre = nombre
                admin.email = email
                admin.save()
                messages.success(request, 'Administrador editado con éxito.')
            except Admin.DoesNotExist:
                messages.error(request, 'Administrador no encontrado.')

        # Bloquear cliente
        elif 'bloquear_cliente' in request.POST:
            cliente_id = request.POST.get('cliente_id')
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                # Agregar entrada en User_block
                User_block.objects.create(usuario_id=cliente.id, es_cliente=True)
                messages.success(request, 'Cliente bloqueado con éxito.')
            except Cliente.DoesNotExist:
                messages.error(request, 'Cliente no encontrado.')

        # Desbloquear cliente
        elif 'desbloquear_cliente' in request.POST:
            cliente_id = request.POST.get('cliente_id')
            try:
                # Eliminar entrada en User_block
                User_block.objects.filter(usuario_id=cliente_id, es_cliente=True).delete()
                messages.success(request, 'Cliente desbloqueado con éxito.')
            except Exception as e:
                messages.error(request, 'Error al desbloquear cliente: ' + str(e))

        # Bloquear administrador
        elif 'bloquear_admin' in request.POST:
            admin_id = request.POST.get('admin_id')
            try:
                admin = Admin.objects.get(id=admin_id)
                # Agregar entrada en User_block
                User_block.objects.create(usuario_id=admin.id, es_cliente=False)
                messages.success(request, 'Administrador bloqueado con éxito.')
            except Admin.DoesNotExist:
                messages.error(request, 'Administrador no encontrado.')

        # Desbloquear administrador
        elif 'desbloquear_admin' in request.POST:
            admin_id = request.POST.get('admin_id')
            try:
                # Eliminar entrada en User_block
                User_block.objects.filter(usuario_id=admin_id, es_cliente=False).delete()
                messages.success(request, 'Administrador desbloqueado con éxito.')
            except Exception as e:
                messages.error(request, 'Error al desbloquear administrador: ' + str(e))

        # Eliminar cliente
        elif 'eliminar_cliente' in request.POST:
            cliente_id = request.POST.get('cliente_id')
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                cliente.delete()
                messages.success(request, 'Cliente eliminado con éxito.')
            except Cliente.DoesNotExist:
                messages.error(request, 'Cliente no encontrado.')

        # Eliminar administrador
        elif 'eliminar_admin' in request.POST:
            admin_id = request.POST.get('admin_id')
            try:
                admin = Admin.objects.get(id=admin_id)
                admin.delete()
                messages.success(request, 'Administrador eliminado con éxito.')
            except Admin.DoesNotExist:
                messages.error(request, 'Administrador no encontrado.')
    
     # Cambiar contraseña de Cliente
    if 'cambiar_contrasena_cliente' in request.POST:
        usuario_id = request.POST.get('usuario_id')
        nueva_contrasena = request.POST.get('nueva_contrasena')
        try:
            cliente = Cliente.objects.get(id=usuario_id)
            cliente.password = make_password(nueva_contrasena)  # Encripta la contraseña para Cliente
            cliente.save()
            messages.success(request, 'Contraseña de cliente cambiada con éxito.')
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente no encontrado.')

    # Cambiar contraseña de Admin
    elif 'cambiar_contrasena_admin' in request.POST:
        usuario_id = request.POST.get('usuario_id')
        nueva_contrasena = request.POST.get('nueva_contrasena')
        try:
            admin = Admin.objects.get(id=usuario_id)
            admin.password = make_password(nueva_contrasena)  # Encripta la contraseña para Admin
            admin.save()
            messages.success(request, 'Contraseña de administrador cambiada con éxito.')
        except Admin.DoesNotExist:
            messages.error(request, 'Administrador no encontrado.')

    # Obtener usuarios bloqueados
    usuarios_bloqueados = User_block.objects.all()
    clientes_bloqueados = []
    admins_bloqueados = []

    for bloqueo in usuarios_bloqueados:
        if bloqueo.es_cliente:
            try:
                cliente = Cliente.objects.get(id=bloqueo.usuario_id)
                clientes_bloqueados.append(cliente)
            except Cliente.DoesNotExist:
                pass
        else:
            try:
                admin = Admin.objects.get(id=bloqueo.usuario_id)
                admins_bloqueados.append(admin)
            except Admin.DoesNotExist:
                pass
    # Renderiza la plantilla con los clientes y administradores
    return render(request, 'gestionar_usuarios.html', {
       'clientes': clientes,
       'admins': admins,
       'bloqueados': bloqueados,
       'clientes_bloqueados': clientes_bloqueados,
       'admins_bloqueados': admins_bloqueados
    })

# Vista para login de gestionar usuarios
def gestion_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin = Admin_user.objects.get(email=email)

            # Verificar la contraseña
            if check_password(password, admin.password):  # Comprobar si la contraseña es correcta
                request.session['admin_id'] = admin.id  # Guardar el ID del admin en la sesión
                return redirect('gestionar_usuarios')  # Redirigir al panel de control de usuarios
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')

        except Admin_user.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos .')

    return render(request, 'gestion_login.html')

# Vista para cerrar sesión
def logout(request):
    request.session.flush()  # Eliminar todas las sesiones
    return redirect('index')  # Redirigir a la página de inicio