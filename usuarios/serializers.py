from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Colaborador, Cargo, Equipe

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = '__all__'

# Serializer para o modelo User, para mostrar detalhes dentro do Colaborador
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ColaboradorSerializer(serializers.ModelSerializer):
    # Usamos os serializers aninhados para mostrar os dados completos, não apenas os IDs
    usuario = UserSerializer(read_only=True)
    cargo = CargoSerializer(read_only=True)
    equipe = EquipeSerializer(read_only=True)

    class Meta:
        model = Colaborador
        # Lista dos campos que serão retornados pela API
        fields = ['usuario', 'cargo', 'equipe', 'data_admissao', 'foto_perfil']