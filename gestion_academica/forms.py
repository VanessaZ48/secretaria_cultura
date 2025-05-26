from django import forms
from gestion_academica.models import ProgramaArtistico

class InscripcionForm(forms.Form):
    programa = forms.ModelChoiceField(queryset=ProgramaArtistico.objects.all(), label="Curso")
