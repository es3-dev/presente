from django.db import models
from management.models import Departamento, Cargo
import qrcode
from io import BytesIO
from django.core.files import File

# Create your models here.

class Reunion(models.Model):
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        creating = self._state.adding  # Saber si es creación
        super().save(*args, **kwargs)
        if creating and not self.qr_code:
            url = f'http://localhost:8000/reunion/asistencia_reunion/{self.id}'
            qr = qrcode.make(url)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            self.qr_code.save(f'reunion_{self.id}.png', File(buffer), save=False)
            # Guardar solo si se generó el QR
            super().save(update_fields=['qr_code'])

    def __str__(self):
        return f'{self.titulo} {self.descripcion}'


class Asistencia(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50)
    documento = models.BigIntegerField()
    email = models.EmailField()
    cargo = models.ForeignKey(Cargo, on_delete=models.DO_NOTHING)
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre} {self.codigo}'

