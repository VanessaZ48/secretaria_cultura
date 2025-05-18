from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .models import ProgramaArtistico, Estudiante, Calificacion
from .serializers import ProgramaArtisticoSerializer, EstudianteSerializer, CalificacionSerializer
from .permissions import IsDocente, IsEstudiante, IsAdministrador

class ProgramaArtisticoViewSet(viewsets.ModelViewSet):
    queryset = ProgramaArtistico.objects.all()
    serializer_class = ProgramaArtisticoSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]  # Solo admins pueden gestionar programas

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated, IsAdministrador]  # Solo admins pueden gestionar estudiantes

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated, IsDocente]  # Solo docentes pueden calificar

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
    

