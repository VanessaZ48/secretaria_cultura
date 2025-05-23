from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse


# ======================
# Autenticación y Login
# ======================

def login_view(request):
    # Si ya está autenticado, redirigir según su grupo
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Administrador').exists():
            return redirect('administrador')
        elif request.user.groups.filter(name='Docente').exists():
            return redirect('vista_notas_docente')
        elif request.user.groups.filter(name='Estudiante').exists():
            return redirect('vista_notas_estudiante')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='Administrador').exists():
                return redirect('administrador')
            elif user.groups.filter(name='Docente').exists():
                return redirect('vista_notas_docente')
            elif user.groups.filter(name='Estudiante').exists():
                return redirect('vista_notas_estudiante')
            else:
                return HttpResponse("No tienes un grupo asignado.")
        else:
            return render(request, 'usuarios/login.html', {
                'error': 'Usuario o contraseña incorrectos',
                'es_login': True
            })

    return render(request, 'usuarios/login.html', {'es_login': True})


def logout_view(request):
    logout(request)
    return redirect('login')


def logout_to_secretaria(request):
    logout(request)
    return redirect('secretaria_inicio')


# ======================
# Permiso de Administrador
# ======================

def es_admin(user):
    return user.is_authenticated and user.groups.filter(name='Administrador').exists()


@login_required
@user_passes_test(es_admin)
def administrador(request):
    grupo = request.user.groups.first().name if request.user.groups.exists() else 'Sin grupo'
    datos = {'grupo': grupo}
    return render(request, 'usuarios/administrador.html', datos)


# ======================
# Vistas de Docente y Estudiante
# ======================

@login_required
def vista_notas_docente(request):
    return render(request, 'usuarios/docente.html')


@login_required
def vista_notas_estudiante(request):
    notas = [
        {'asignatura': 'Matemáticas', 'nota': 3.5},
        {'asignatura': 'Historia', 'nota': 2.5},
        {'asignatura': 'Lengua', 'nota': 4.0},
    ]
    return render(request, 'usuarios/estudiante.html', {'notas': notas})


# ======================
# Funcionalidades de Gestión Académica
# ======================

@login_required
def ingresar_notas(request):
    return render(request, 'usuarios/ingresar_notas.html')


@login_required
def ver_estudiantes(request):
    return render(request, 'usuarios/ver_estudiantes.html')


# ======================
# Páginas Públicas
# ======================

def secretaria_inicio(request):
    return render(request, 'usuarios/secretaria_inicio.html')


def inscribir_curso(request):
    return render(request, 'usuarios/inscribir_curso.html')


def inscripcion_exitosa(request):
    return render(request, 'usuarios/inscripcion_exitosa.html')
