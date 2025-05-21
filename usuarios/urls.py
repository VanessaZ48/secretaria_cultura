from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('administrador/', views.administrador, name='administrador'),
    path('docente/', views.vista_notas_docente, name='vista_notas_docente'),
    path('notas/estudiante/', views.vista_notas_estudiante, name='vista_notas_estudiante'),
    path('ingresar-notas/', views.ingresar_notas, name='ingresar_notas'),  
    path('ver-estudiantes/', views.ver_estudiantes, name='ver_estudiantes'),
    path('secretaria/', views.secretaria_inicio, name='secretaria_inicio'),
    path('inscribir_curso/', views.inscribir_curso, name='inscripcion'),
    path('inscripcion_exitosa/', views.inscripcion_exitosa, name='inscripcion_exitosa'),
    
    
    
]
