from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from gestion_academica.models import Estudiante, ProgramaArtistico, Calificacion


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
    cursos = ProgramaArtistico.objects.all()
    estudiantes = []
    curso_seleccionado = request.GET.get('curso')
    periodo = request.GET.get('periodo')
    corte = request.GET.get('corte')  # Solo para filtros

    if curso_seleccionado and periodo and corte:
        estudiantes = Estudiante.objects.filter(
            programa__nombre=curso_seleccionado
        ).order_by('nombre')

        # Agregar calificación previa si existe
        for estudiante in estudiantes:
            estudiante.nota = Calificacion.objects.filter(
                estudiante=estudiante,
                periodo=periodo
            ).first()

    if request.method == 'POST':
        estudiantes_ids = request.POST.getlist('estudiante_id')
        periodo = request.POST.get('periodo')

        for est_id in estudiantes_ids:
            nota_valor = request.POST.get(f'nota_{est_id}')
            observacion = request.POST.get(f'observacion_{est_id}', '')

            if nota_valor:
                try:
                    nota_valor = float(nota_valor)
                    Calificacion.objects.update_or_create(
                        estudiante_id=est_id,
                        periodo=periodo,
                        defaults={
                            'nota': nota_valor,
                            'observaciones': observacion
                        }
                    )
                except ValueError:
                    continue  # Si nota no es un número, ignorar

        messages.success(request, "Notas guardadas correctamente.")
        return redirect(request.path + f"?curso={curso_seleccionado}&periodo={periodo}&corte={corte}")

    context = {
        'cursos': cursos,
        'estudiantes': estudiantes,
        'curso_seleccionado': curso_seleccionado,
        'periodo': periodo,
        'corte': corte,
    }
    return render(request, 'usuarios/ingresar_notas.html', context)

@login_required
def ver_estudiantes(request):
    estudiantes = Estudiante.objects.select_related('programa').all().order_by('nombre')
    programas = ProgramaArtistico.objects.all().order_by('nombre')
    return render(request, 'usuarios/ver_estudiantes.html', {
        'estudiantes': estudiantes,
        'programas': programas
    })


# ======================
# Páginas Públicas
# ======================

def secretaria_inicio(request):
    return render(request, 'usuarios/secretaria_inicio.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from gestion_academica.models import ProgramaArtistico, Inscripcion


def inscripcion_view(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        nombre_curso = request.POST.get('curso')
        correo = request.POST.get('correo')
        comentarios = request.POST.get('comentarios')
        fecha_inscripcion = request.POST.get('fecha_inscripcion')


        if not nombre_curso:
            messages.error(request, "Debe seleccionar un curso.")
            return redirect('inscribir_curso')

        try:
            programa = ProgramaArtistico.objects.get(nombre=nombre_curso)

            Inscripcion.objects.create(
                nombre=nombre,
                apellido=apellido,
                curso=programa,
                correo=correo,
                comentarios=comentarios,
                fecha_inscripcion=fecha_inscripcion
            )

            messages.success(
                request,
                f"Inscripción exitosa en {programa.nombre} para {nombre} {apellido}"
            )

        except ProgramaArtistico.DoesNotExist:
            messages.error(request, "El curso seleccionado no existe.")

        return redirect('inscribir_curso')

    else:
        cursos = ProgramaArtistico.objects.all()
        return render(request, 'usuarios/inscribir_curso.html', {'cursos': cursos})

