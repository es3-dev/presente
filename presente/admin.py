from django.contrib import admin
from management.models import Departamento, Cargo, Empleado
from .models import Reunion, Asistencia
# Register your models here.
admin.site.register(Departamento)
admin.site.register(Cargo)
admin.site.register(Empleado)
admin.site.register(Reunion)
admin.site.register(Asistencia)