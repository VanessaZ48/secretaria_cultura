from django.urls import path
from . import views
from .views import ingresar_notas
from .views import secretaria_inicio


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('docente/', views.vista_notas_docente, name='vista_notas_docente'),
    path('notas/estudiante/', views.vista_notas_estudiante, name='vista_notas_estudiante'),
    path('admin/general/', views.vista_administrador, name='vista_administrador'),
    path('logout/', views.logout_view, name='logout'),
    path('ingresar-notas/', ingresar_notas, name='ingresar_notas'),  
    path('ver-estudiantes/', views.ver_estudiantes, name='ver_estudiantes'),
    path('secretaria/', views.secretaria_inicio, name='secretaria_inicio'),
    
]
