from rest_framework import serializers
from .models import ProgramaArtistico, Estudiante, Calificacion, Inscripcion

class ProgramaArtisticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaArtistico
        fields = '__all__'

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'