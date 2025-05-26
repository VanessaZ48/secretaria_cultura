from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProgramaArtistico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(unique=True)
    documento = models.CharField(max_length=20, unique=True)
    programa = models.ForeignKey(ProgramaArtistico, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=10)
    nota = models.FloatField()
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('estudiante', 'periodo')  # Evita duplicados

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.periodo}: {self.nota}"


class Docente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    programas = models.ManyToManyField(ProgramaArtistico)

    def __str__(self):
        return self.usuario.username
    

class Inscripcion(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)  
    curso = models.ForeignKey(ProgramaArtistico, on_delete=models.CASCADE)
    correo = models.EmailField()
    comentarios = models.TextField(blank=True, null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.curso.nombre}"
