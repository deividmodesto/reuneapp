# reune_app/avaliacoes/views.py

from rest_framework import viewsets
from .models import CicloAvaliacao, Competencia, RespostaAvaliacao
from .serializers import CicloAvaliacaoSerializer, CompetenciaSerializer, RespostaAvaliacaoSerializer

class CicloAvaliacaoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar Ciclos de Avaliação.
    """
    queryset = CicloAvaliacao.objects.all()
    serializer_class = CicloAvaliacaoSerializer

class CompetenciaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar Competências.
    """
    queryset = Competencia.objects.all()
    serializer_class = CompetenciaSerializer

class RespostaAvaliacaoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar Respostas de Avaliação.
    """
    # .select_related otimiza a consulta, buscando os dados relacionados de uma vez
    queryset = RespostaAvaliacao.objects.select_related(
        'ciclo', 'avaliado', 'avaliador', 'competencia'
    ).all()
    serializer_class = RespostaAvaliacaoSerializer