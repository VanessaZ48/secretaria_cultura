from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from django.utils.decorators import method_decorator

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Docente').exists():
                return redirect('vista_notas_docente')
            elif user.groups.filter(name='Estudiante').exists():
                return redirect('vista_notas_estudiante')
            else:
                return HttpResponse("No tienes un grupo asignado.")
        else:
            return render(request, 'usuarios/login.html', {'error': 'Usuario o contraseña incorrectos'})
    
    return render(request, 'usuarios/login.html')

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
def vista_administrador(request):
    return HttpResponse("Bienvenido Administrador. Panel general.")

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


@login_required
def secretaria_inicio(request):
    return render(request, 'usuarios/secretaria_inicio.html')

