from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ProgramaArtistico, Estudiante, Calificacion, Docente
from .serializers import (
    ProgramaArtisticoSerializer,
    EstudianteSerializer,
    CalificacionSerializer
)
from .permissions import IsDocente, IsEstudiante, IsAdministrador

# -------------------------------------------------------------------
# VISTAS BASADAS EN CLASES (APIView / ViewSet)
# -------------------------------------------------------------------

# --- Programa Artístico (solo admins)
class ProgramaArtisticoViewSet(viewsets.ModelViewSet):
    queryset = ProgramaArtistico.objects.all()
    serializer_class = ProgramaArtisticoSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]

# --- Estudiantes (solo admins)
class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]

# --- Calificaciones (solo docentes)
class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated, IsDocente]

# --- Cargar varias notas (solo docentes)
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

# --- Vista protegida genérica
class MiVistaProtegida(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"mensaje": "Solo usuarios autenticados pueden ver esto"})

# --- Ver programas del docente autenticado
class MisProgramasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        docente = Docente.objects.get(usuario=request.user)
        programas = docente.programas.all()
        serializer = ProgramaArtisticoSerializer(programas, many=True)
        return Response(serializer.data)

# --- Ver estudiantes por programa (si el docente tiene acceso)
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

# --- Ver lista de estudiantes (HTML)
def ver_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'usuarios/ver_estudiantes.html', {'estudiantes': estudiantes})

# --- Vista de inicio para Secretaría de Cultura (HTML)
def inicio_secretaria(request):
    return render(request, 'usuarios/secretaria_inicio.html')
