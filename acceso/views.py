from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import RegistroAcceso, Apoderado


@login_required
def index(request):
    # Si el usuario es portero (no es staff), redirigir directamente al escáner
    if not request.user.is_staff:
        return redirect('escaner')
    return render(request, 'index.html')


@login_required
def vista_escaner(request):
    return render(request, 'acceso/escaner.html')


@login_required
def validar_qr(request, rut):
    try:
        apoderado = Apoderado.objects.get(rut=rut)
        alumnos = list(apoderado.alumnos.values('nombre', 'curso'))
        
        RegistroAcceso.objects.create(
            apoderado=apoderado,
            permitido=apoderado.autorizado
        )

        foto_url = apoderado.foto.url if apoderado.foto else None

        data = {
            'valido': True,
            'nombre': apoderado.nombre,
            'rut': apoderado.rut,
            'autorizado': apoderado.autorizado,
            'alumnos': alumnos,
            'foto': foto_url
        }
    except Apoderado.DoesNotExist:
        data = {
            'valido': False,
            'mensaje': f'El RUT {rut} no se encuentra registrado.'
        }
    
    return JsonResponse(data)


@login_required
def historial_acceso(request):
    # Bloquear acceso al historial si el usuario es portero
    if not request.user.is_staff:
        messages.warning(request, "No tienes permisos para consultar el historial de accesos.")
        return redirect('escaner')

    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    fecha = request.GET.get('fecha', '').strip()

    registros_list = RegistroAcceso.objects.select_related('apoderado').prefetch_related('apoderado__alumnos').order_by('-fecha_hora')

    if q:
        registros_list = registros_list.filter(
            Q(apoderado__nombre__icontains=q) |
            Q(apoderado__rut__icontains=q) |
            Q(apoderado__alumnos__nombre__icontains=q) |
            Q(apoderado__alumnos__curso__icontains=q)
        ).distinct()

    if estado == 'permitido':
        registros_list = registros_list.filter(permitido=True)
    elif estado == 'denegado':
        registros_list = registros_list.filter(permitido=False)

    if fecha:
        registros_list = registros_list.filter(fecha_hora__date=fecha)

    paginator = Paginator(registros_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'q': q,
        'estado': estado,
        'fecha': fecha,
    }
    return render(request, 'acceso/historial.html', context)


def login_view(request):
    # Redirigir al usuario autenticado según su rol
    if request.user.is_authenticated:
        if not request.user.is_staff:
            return redirect('escaner')
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido(a), {user.get_full_name() or username}!")
                
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                
                # Si no es staff, llevar directamente al escáner
                if not user.is_staff:
                    return redirect('escaner')
                return redirect('index')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')


@login_required
def politica_privacidad(request):
    return render(request, 'privacidad.html')