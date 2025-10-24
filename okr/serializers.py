# reune_app/okr/serializers.py

from rest_framework import serializers
from .models import Objetivo, ResultadoChave, CheckIn

# Importando o UserSerializer do app de usuarios para reutilizá-lo
from usuarios.serializers import UserSerializer

class CheckInSerializer(serializers.ModelSerializer):
    # Mostra os dados do colaborador ao invés de apenas o ID
    colaborador = UserSerializer(read_only=True)

    class Meta:
        model = CheckIn
        fields = ['id', 'valor_atual', 'nota_confianca', 'comentario', 'data_checkin', 'colaborador']
        # Definimos campos que podem ser preenchidos ao criar um novo check-in via API
        extra_kwargs = {
            'colaborador': {'read_only': True} # O colaborador será o usuário logado, futuramente
        }


class ResultadoChaveSerializer(serializers.ModelSerializer):
    # Aninhando os check-ins dentro de cada resultado-chave
    checkins = CheckInSerializer(many=True, read_only=True)

    class Meta:
        model = ResultadoChave
        fields = ['id', 'descricao', 'tipo', 'valor_inicial', 'valor_alvo', 'checkins']


class ObjetivoSerializer(serializers.ModelSerializer):
    # Aninhando os resultados-chave e mostrando os dados do responsável
    resultados_chave = ResultadoChaveSerializer(many=True, read_only=True)
    responsavel = UserSerializer(read_only=True)

    class Meta:
        model = Objetivo
        fields = ['id', 'titulo', 'descricao', 'ciclo', 'data_criacao', 'responsavel', 'resultados_chave']
        read_only_fields = ['progresso']

        # reune_app/okr/serializers.py

class CheckInSerializer(serializers.ModelSerializer):
    colaborador = UserSerializer(read_only=True)

    class Meta:
        model = CheckIn
        # AQUI ESTÁ A CORREÇÃO: Adicionamos 'resultado_chave' à lista
        fields = ['id', 'resultado_chave', 'valor_atual', 'nota_confianca', 'comentario', 'data_checkin', 'colaborador']
        extra_kwargs = {
            'colaborador': {'read_only': True}
        }

class ResultadoChaveSerializer(serializers.ModelSerializer):
    checkins = CheckInSerializer(many=True, read_only=True)

    class Meta:
        model = ResultadoChave
        # ADICIONE 'progresso' À LISTA ABAIXO
        fields = ['id', 'descricao', 'tipo', 'valor_inicial', 'valor_alvo', 'progresso', 'checkins']
        # O campo progresso será apenas para leitura, pois é calculado automaticamente
        read_only_fields = ['progresso']