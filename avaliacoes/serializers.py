# reune_app/avaliacoes/serializers.py

from rest_framework import serializers
from .models import CicloAvaliacao, Competencia, RespostaAvaliacao

# Reutilizando o serializer de Usuário que já criamos
from usuarios.serializers import UserSerializer

class CicloAvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloAvaliacao
        fields = ['id', 'titulo', 'data_inicio', 'data_fim', 'status']

class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = ['id', 'nome', 'descricao']

class RespostaAvaliacaoSerializer(serializers.ModelSerializer):
    # Usando serializers aninhados para uma resposta mais completa e informativa
    avaliado = UserSerializer(read_only=True)
    avaliador = UserSerializer(read_only=True)
    competencia = CompetenciaSerializer(read_only=True)
    ciclo = CicloAvaliacaoSerializer(read_only=True)

    class Meta:
        model = RespostaAvaliacao
        fields = [
            'id',
            'ciclo',
            'avaliado',
            'avaliador',
            'competencia',
            'nota',
            'justificativa',
            'data_resposta'
        ]