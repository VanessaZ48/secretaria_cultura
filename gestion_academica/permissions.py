from rest_framework.permissions import BasePermission

class IsDocente(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Docentes').exists()

class IsEstudiante(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Estudiantes').exists()

class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Administradores').exists()
