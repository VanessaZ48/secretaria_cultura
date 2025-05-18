from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('notas/docente/', views.vista_notas_docente, name='vista_notas_docente'),
    path('notas/estudiante/', views.vista_notas_estudiante, name='vista_notas_estudiante'),
    path('admin/general/', views.vista_administrador, name='vista_administrador'),
]
