from django.shortcuts import render
from management.models import Empleado, Cargo, Departamento
from presente.models import Reunion, Asistencia
from .serializers import DepartamentoSerializer, CargoSerializer, EmpleadoSerializer, ReunionSerializer, AsistenciaSerializer
from rest_framework import viewsets

# Create your views here.
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    lookup_field = 'documento'

class ReunionViewSet(viewsets.ModelViewSet):
    queryset = Reunion.objects.all()
    serializer_class = ReunionSerializer

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer