from django.db import models

# Create your models here.

class ProgramaArtistico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    documento = models.CharField(max_length=20, unique=True)
    programa = models.ForeignKey(ProgramaArtistico, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=10)
    nota = models.FloatField()
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('estudiante', 'periodo')  # Evita duplicados

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.periodo}: {self.nota}"

