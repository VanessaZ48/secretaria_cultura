from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramaArtisticoViewSet, EstudianteViewSet, CalificacionViewSet, CargarNotasView
from .views import MisProgramasView, EstudiantesPorProgramaView


router = DefaultRouter()
router.register(r'programas', ProgramaArtisticoViewSet)
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'calificaciones', CalificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cargar-notas/', CargarNotasView.as_view(), name='cargar_notas'),

    path('mis-programas/', MisProgramasView.as_view(), name='mis_programas'),
    path('programa/<int:programa_id>/estudiantes/', EstudiantesPorProgramaView.as_view(), name='estudiantes_por_programa'),
    

]
