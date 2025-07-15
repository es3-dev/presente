from django.db import models

# Create your models here.
class Departamento(models.Model):
    nombre_departamento = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre_departamento}'

class Cargo(models.Model):
    cargo = models.CharField(max_length=100)
    salario = models.BigIntegerField()
    departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.cargo}'

class Empleado(models.Model):
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True)
    documento = models.BigIntegerField(unique=True)
    codigo = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.BigIntegerField()
    fecha_contratacion = models.DateField(auto_now_add=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING)
    cargo = models.ForeignKey(Cargo, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.primer_nombre} {self.primer_apellido}'