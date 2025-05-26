from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ProgramaArtistico, Estudiante, Calificacion, Docente, Inscripcion
from .serializers import (
    ProgramaArtisticoSerializer,
    EstudianteSerializer,
    CalificacionSerializer,
)
from .permissions import IsDocente, IsAdministrador


# -------------------------------------------------------------------
# VISTAS API BASADAS EN CLASES
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


class MisProgramasView(APIView):
    permission_classes = [IsAuthenticated, IsDocente]

    def get(self, request):
        docente = Docente.objects.get(usuario=request.user)
        programas = docente.programas.all()
        serializer = ProgramaArtisticoSerializer(programas, many=True)
        return Response(serializer.data)


class EstudiantesPorProgramaView(APIView):
    permission_classes = [IsAuthenticated, IsDocente]

    def get(self, request, programa_id):
        docente = Docente.objects.get(usuario=request.user)

        if not docente.programas.filter(id=programa_id).exists():
            return Response({'error': 'No autorizado para ver este programa'}, status=403)

        estudiantes = Estudiante.objects.filter(programa__id=programa_id)
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)


class CargarNotasView(APIView):
    permission_classes = [IsAuthenticated, IsDocente]

    def post(self, request):
        datos = request.data
        exitosas = []
        errores = []

        if not isinstance(datos, list):
            return Response(
                {"error": "Debe enviar una lista de notas"},
                status=status.HTTP_400_BAD_REQUEST
            )

        docente = Docente.objects.get(usuario=request.user)

        for item in datos:
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

                if not docente.programas.filter(id=estudiante.programa.id).exists():
                    errores.append({
                        "documento": documento,
                        "error": "No autorizado para calificar a este estudiante"
                    })
                    continue

                calificacion, _ = Calificacion.objects.update_or_create(
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

        status_code = status.HTTP_201_CREATED if exitosas else status.HTTP_400_BAD_REQUEST
        return Response({
            "notas_registradas": exitosas,
            "errores": errores
        }, status=status_code)


# -------------------------------------------------------------------
# VISTAS HTML (basadas en funciones)
# -------------------------------------------------------------------


def ver_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'usuarios/ver_estudiantes.html', {'estudiantes': estudiantes})



def inicio_secretaria(request):
    return render(request, 'usuarios/secretaria_inicio.html')


def administrador(request):
    return render(request, 'usuarios/administrador.html')


def inscripcion_view(request):
    programas = ProgramaArtistico.objects.all()
    return render(request, 'usuarios/inscribir_curso.html', {'programas': programas})
