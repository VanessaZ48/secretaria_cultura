from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProgramaArtistico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(unique=True)
    documento = models.CharField(max_length=20, unique=True)
    programa = models.ForeignKey(ProgramaArtistico, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Calificacion(models.Model):
    estudiante = models.ForeignKey(
        'Estudiante',  # Relación con modelo Estudiante
        on_delete=models.CASCADE,
        related_name='calificaciones'
    )
    periodo = models.CharField(
        max_length=10,
        help_text="Periodo académico, e.g. '2024-1', '2024-2'"
    )
    nota = models.FloatField(
        help_text="Nota obtenida por el estudiante en el periodo"
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        help_text="Observaciones adicionales sobre la calificación"
    )

    class Meta:
        unique_together = ('estudiante', 'periodo')  # Evita calificaciones duplicadas para un mismo estudiante y periodo
        ordering = ['estudiante', 'periodo']  # Ordena por estudiante y periodo por defecto
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.periodo}: {self.nota}"



class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.apellido}: {self.email}"
    

class Inscripcion(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)  # Asegúrate de tener este campo
    curso = models.ForeignKey(ProgramaArtistico, on_delete=models.CASCADE)
    correo = models.EmailField()
    comentarios = models.TextField(blank=True, null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    # Nuevo campo estado
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('rechazado', 'Rechazado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.curso.nombre}"