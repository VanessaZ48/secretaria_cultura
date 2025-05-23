from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    Inscripcion,
    ProgramaArtistico,
    Estudiante,
    Calificacion,
    Docente
)

from .serializers import (
    ProgramaArtisticoSerializer,
    EstudianteSerializer,
    CalificacionSerializer,
    InscripcionSerializer
)

from .permissions import IsDocente, IsEstudiante, IsAdministrador

# -------------------------------------------------------------------
# VISTAS BASADAS EN CLASES (APIView / ViewSet)
# -------------------------------------------------------------------

class ProgramaArtisticoViewSet(viewsets.ModelViewSet):
    queryset = ProgramaArtistico.objects.all()
    serializer_class = ProgramaArtisticoSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]


class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]


class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated, IsDocente]


class CargarNotasView(APIView):
    permission_classes = [IsAuthenticated, IsDocente]

    def post(self, request):
        notas = request.data
        exitosas = []
        errores = []

        if not isinstance(notas, list) or not notas:
            return Response(
                {"error": "Debe enviar una lista de notas no vacía"},
                status=status.HTTP_400_BAD_REQUEST
            )

        for item in notas:
            documento = item.get("documento")
            periodo = item.get("periodo")
            nota = item.get("nota")
            observaciones = item.get("observaciones", "")

            if not all([documento, periodo, nota is not None]):
                errores.append({
                    "documento": documento,
                    "error": "Faltan campos requeridos (documento, periodo o nota)"
                })
                continue

            try:
                estudiante = Estudiante.objects.get(documento=documento)
                calificacion, creada = Calificacion.objects.update_or_create(
                    estudiante=estudiante,
                    periodo=periodo,
                    defaults={
                        "nota": nota,
                        "observaciones": observaciones
                    }
                )
                exitosas.append(CalificacionSerializer(calificacion).data)

            except Estudiante.DoesNotExist:
                errores.append({
                    "documento": documento,
                    "error": "Estudiante no encontrado"
                })
            except Exception as e:
                errores.append({
                    "documento": documento,
                    "error": str(e)
                })

        status_code = status.HTTP_201_CREATED if exitosas else status.HTTP_400_BAD_REQUEST

        return Response(
            {
                "notas_registradas": exitosas,
                "errores": errores
            },
            status=status_code
        )


class MiVistaProtegida(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"mensaje": "Solo usuarios autenticados pueden ver esto"})


class MisProgramasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        docente = Docente.objects.get(usuario=request.user)
        programas = docente.programas.all()
        serializer = ProgramaArtisticoSerializer(programas, many=True)
        return Response(serializer.data)


class EstudiantesPorProgramaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, programa_id):
        docente = Docente.objects.get(usuario=request.user)
        if not docente.programas.filter(id=programa_id).exists():
            return Response({'error': 'No autorizado para ver este programa'}, status=403)

        estudiantes = Estudiante.objects.filter(programa__id=programa_id)
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)


# -------------------------------------------------------------------
# VISTAS BASADAS EN FUNCIONES (HTML / Render)
# -------------------------------------------------------------------

def ver_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'usuarios/ver_estudiantes.html', {'estudiantes': estudiantes})


def inicio_secretaria(request):
    return render(request, 'usuarios/secretaria_inicio.html')


def administrador(request):
    return render(request, 'usuarios/administrador.html')


from django.shortcuts import render, redirect
from django.contrib import messages

def inscripcion_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        curso = request.POST.get('curso')
        correo = request.POST.get('correo')
        comentarios = request.POST.get('comentarios')

        # Aquí podrías guardar la información en la base de datos si lo necesitas

        messages.success(request, '¡Inscripción exitosa! Gracias por registrarte.')
        return redirect('inscribir_curso')  # Esto recarga el formulario limpio

    return render(request, 'inscribir_curso.html')