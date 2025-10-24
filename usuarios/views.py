# reune_app/usuarios/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action # <-- IMPORTE O 'action'
from rest_framework.response import Response # <-- IMPORTE O 'Response'
from .models import Colaborador, Cargo, Equipe
from .serializers import ColaboradorSerializer, CargoSerializer, EquipeSerializer
# Importando modelos de outros apps que vamos precisar
from avaliacoes.models import CicloAvaliacao, RespostaAvaliacao
from django.db.models import Avg

class CargoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que cargos sejam visualizados ou editados.
    """
    queryset = Cargo.objects.all().order_by('titulo')
    serializer_class = CargoSerializer
    # Futuramente, adicionaremos permissões aqui

class EquipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que equipes sejam visualizadas ou editadas.
    """
    queryset = Equipe.objects.all().order_by('nome')
    serializer_class = EquipeSerializer
    # Futuramente, adicionaremos permissões aqui

class ColaboradorViewSet(viewsets.ModelViewSet):
    queryset = Colaborador.objects.select_related('usuario', 'cargo', 'equipe').all()
    serializer_class = ColaboradorSerializer

    @action(detail=True, methods=['get'], url_path='relatorio-avaliacao')
    def relatorio_avaliacao(self, request, pk=None):
        """
        Gera um relatório de desempenho para um colaborador específico
        em um determinado ciclo de avaliação.
        Exemplo de URL: /api/usuarios/colaboradores/1/relatorio-avaliacao/?ciclo_id=2
        """
        # 1. Pega o objeto do colaborador (pk é o ID vindo da URL)
        colaborador = self.get_object()
        
        # 2. Pega o ID do ciclo dos parâmetros da URL
        ciclo_id = request.query_params.get('ciclo_id', None)
        
        if not ciclo_id:
            return Response(
                {"error": "O parâmetro 'ciclo_id' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            ciclo = CicloAvaliacao.objects.get(pk=ciclo_id)
            # 3. Filtra todas as respostas de avaliação para este colaborador neste ciclo
            respostas = RespostaAvaliacao.objects.filter(
                avaliado=colaborador.usuario,
                ciclo=ciclo
            )

            if not respostas.exists():
                return Response(
                    {"message": "Nenhuma avaliação encontrada para este colaborador neste ciclo."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 4. Agrupa as respostas por competência para calcular as médias
            # O .values() agrupa, o .annotate() calcula a média para cada grupo
            sumario_competencias = respostas.values('competencia__nome').annotate(
                media_notas=Avg('nota')
            ).order_by('competencia__nome')

            # 5. Monta a resposta final em um formato legível
            dados_relatorio = {
                'colaborador': colaborador.usuario.get_full_name(),
                'ciclo_avaliacao': ciclo.titulo,
                'sumario': [
                    {
                        'competencia': item['competencia__nome'],
                        'media_notas': round(item['media_notas'], 2)
                    } for item in sumario_competencias
                ],
                'comentarios': list(respostas.exclude(justificativa__exact='')
                                              .values_list('justificativa', flat=True))
            }
            
            return Response(dados_relatorio)

        except CicloAvaliacao.DoesNotExist:
            return Response(
                {"error": f"Ciclo de avaliação com id={ciclo_id} não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
