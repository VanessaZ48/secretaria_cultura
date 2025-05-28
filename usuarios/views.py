from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from gestion_academica.models import Estudiante, ProgramaArtistico, Calificacion, Docente, User, Inscripcion
from django.db.models import Count


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
    cursos = ProgramaArtistico.objects.all()
    docentes = Docente.objects.all()
    total_cursos = cursos.count()
    total_docentes = docentes.count()
    total_estudiantes = Estudiante.objects.count()
    inscripciones = Inscripcion.objects.select_related('curso').all()
    total_inscripciones_pendientes = inscripciones.count()

    # Estadísticas de estudiantes por curso
    cursos_con_estudiantes = (
        ProgramaArtistico.objects
        .annotate(num_estudiantes=Count('estudiante'))
        .values('nombre', 'num_estudiantes')
    )

    # Extraer listas para los gráficos
    nombres_cursos = [curso['nombre'] for curso in cursos_con_estudiantes]
    total_estudiantes_por_curso = [curso['num_estudiantes'] for curso in cursos_con_estudiantes]

    context = {
        'cursos': cursos,
        'docentes': docentes,
        'total_cursos': total_cursos,
        'total_docentes': total_docentes,
        'total_estudiantes': total_estudiantes,
        'inscripciones': inscripciones,
        'total_inscripciones_pendientes': total_inscripciones_pendientes,
        'nombres_cursos': nombres_cursos,
        'total_estudiantes_por_curso': total_estudiantes_por_curso,
    }

    return render(request, 'usuarios/administrador.html', context)

# ======================
# Vistas de Docente y Estudiante
# ======================

@login_required
def vista_notas_docente(request):
    return render(request, 'usuarios/docente.html')


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def vista_notas_estudiante(request):
    # Obtener el estudiante asociado al usuario logueado
    estudiante = get_object_or_404(Estudiante, usuario=request.user)

    # Obtener las calificaciones del estudiante (puedes mostrar todas o filtrar por periodo, etc.)
    calificaciones = estudiante.calificaciones.all()

    # Construir la lista de notas para pasar al template
    notas = []
    for cal in calificaciones:
        notas.append({
            'asignatura': estudiante.programa.nombre,
            'nota': cal.nota,
            'periodo': cal.periodo,
        })

    # Pasar también el estudiante y programa para mostrar nombre y curso en el template
    contexto = {
        'notas': notas,
        'estudiante': estudiante,
        'programa': estudiante.programa,
    }
    return render(request, 'usuarios/estudiante.html', contexto)


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

