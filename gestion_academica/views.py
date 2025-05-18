from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
    def post(self, request):
        notas_data = request.data

        if not isinstance(notas_data, list):
            return Response(
                {"error": "Se esperaba una lista de notas"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(notas_data) == 0:
            return Response(
                {"error": "No se enviaron notas"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CalificacionSerializer(data=notas_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"mensaje": "Notas cargadas correctamente"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
