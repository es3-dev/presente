from rest_framework import serializers
from management.models import Departamento, Cargo, Empleado
from presente.models import Reunion, Asistencia

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    cargo = CargoSerializer() 
    departamento = DepartamentoSerializer()

    class Meta:
        model = Empleado
        fields = [
            'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
            'documento', 'codigo', 'email', 'telefono', 'fecha_contratacion',
            'cargo', 'departamento'
        ]

class ReunionSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer()

    class Meta:
        model = Reunion
        fields = '__all__'

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'