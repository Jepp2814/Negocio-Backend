from rest_framework import serializers
from .models import Cuenta, CategoriaFinanciera, MovimientoFinanciero

class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = '__all__'

class CategoriaFinancieraSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaFinanciera
        fields = '__all__'

class MovimientoFinancieroSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoFinanciero
        fields = '__all__'

