# reune_app/clima/serializers.py

from rest_framework import serializers
from .models import RegistroHumor
from usuarios.serializers import UserSerializer

class RegistroHumorSerializer(serializers.ModelSerializer):
    # Campo extra para mostrar o texto do humor (ex: "Feliz") e não só o número (ex: 4)
    humor_texto = serializers.CharField(source='get_humor_display', read_only=True)
    colaborador = UserSerializer(read_only=True)

    class Meta:
        model = RegistroHumor
        fields = [
            'id',
            'colaborador',
            'data_registro',
            'humor',
            'humor_texto', # Adicionamos o campo extra aqui
            'comentario'
        ]