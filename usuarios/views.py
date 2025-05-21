from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

def login_view(request):
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
            return render(request, 'usuarios/login.html', {'error': 'Usuario o contraseña incorrectos'})
    
    return render(request, 'usuarios/login.html')

def es_admin(user):
    return user.is_authenticated and user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(es_admin)
def administrador(request):
    grupo = request.user.groups.first().name if request.user.groups.exists() else 'Sin grupo'
    datos = { 'grupo': grupo }
    return render(request, 'usuarios/administrador.html', datos)

@login_required
def vista_notas_docente(request):
    return render(request, 'usuarios/docente.html')

@login_required
def vista_notas_estudiante(request):
    notas = [
        {'asignatura': 'Matemáticas', 'nota': 3.5},
        {'asignatura': 'Historia', 'nota': 2.5 },
        {'asignatura': 'Lengua', 'nota': 4.0},
    ]
    return render(request, 'usuarios/estudiante.html', {'notas': notas})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def ingresar_notas(request):
    return render(request, 'usuarios/ingresar_notas.html')

@login_required
def ver_estudiantes(request):
    return render(request, 'usuarios/ver_estudiantes.html')


def secretaria_inicio(request):
    return render(request, 'usuarios/secretaria_inicio.html')

def inscribir_curso(request):
    return render(request, 'usuarios/inscribir_curso.html')

