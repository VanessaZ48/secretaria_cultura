from django import forms
from gestion_academica.models import ProgramaArtistico
from .models import Calificacion

class InscripcionForm(forms.Form):
    programa = forms.ModelChoiceField(queryset=ProgramaArtistico.objects.all(), label="Curso")


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['nota', 'observaciones']
        widgets = {
            'nota': forms.NumberInput(attrs={'step': '0.01', 'min': 0, 'max': 5}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }