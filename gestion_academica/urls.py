from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramaArtisticoViewSet, EstudianteViewSet, CalificacionViewSet, CargarNotasView
from .views import CargarNotasView

router = DefaultRouter()
router.register(r'programas', ProgramaArtisticoViewSet)
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'calificaciones', CalificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cargar-notas/', CargarNotasView.as_view(), name='cargar_notas'),
]


