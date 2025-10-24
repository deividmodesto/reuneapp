# reune_app/okr/views.py

# Imports necessários
from django.db.models import Avg
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Objetivo, ResultadoChave, CheckIn
from .serializers import ObjetivoSerializer, ResultadoChaveSerializer, CheckInSerializer
from rest_framework import permissions # <-- VERIFIQUE SE ESTE IMPORT EXISTE
from .permissions import IsOwnerOrReadOnly # <-- IMPORTE NOSSA NOVA CLASSE

class ObjetivoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar Objetivos.
    """
    queryset = Objetivo.objects.prefetch_related('resultados_chave__checkins', 'responsavel').all()
    serializer_class = ObjetivoSerializer
    # permission_classes = [IsAuthenticated] # Adicionaremos no futuro

def get_queryset(self):
        # ... (o método get_queryset que criamos antes continua exatamente o mesmo) ...
        usuario_logado = self.request.user
        if not usuario_logado.is_authenticated:
            return Objetivo.objects.none()

        query_visivel = Q(responsavel=usuario_logado)

        equipes_lideradas = Equipe.objects.filter(lider=usuario_logado)
        if equipes_lideradas.exists():
            membros_ids = []
            for equipe in equipes_lideradas:
                membros_ids.extend(equipe.membros.values_list('usuario_id', flat=True))
            
            if membros_ids:
                query_visivel |= Q(responsavel_id__in=membros_ids)

        return Objetivo.objects.filter(query_visivel).distinct()


class ResultadoChaveViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar Resultados-Chave.
    """
    queryset = ResultadoChave.objects.prefetch_related('checkins').all()
    serializer_class = ResultadoChaveSerializer
    # permission_classes = [IsAuthenticated] # Adicionaremos no futuro

class CheckInViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e editar Check-ins, com lógica de negócio customizada.
    """
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    # permission_classes = [IsAuthenticated] # Adicionaremos no futuro

    def perform_create(self, serializer):
        # --- Parte 1: Atualizar o Resultado-Chave ---
        resultado_chave = serializer.validated_data['resultado_chave']
        valor_checkin = serializer.validated_data['valor_atual']
        
        resultado_chave.valor_atual = valor_checkin
        
        try:
            range_total = resultado_chave.valor_alvo - resultado_chave.valor_inicial
            range_atual = valor_checkin - resultado_chave.valor_inicial
            if range_total == 0:
                progresso = 100.00 if range_atual >= 0 else 0.00
            else:
                progresso = (range_atual / range_total) * 100
            resultado_chave.progresso = max(0, min(progresso, 100))
        except (ValueError, TypeError):
            resultado_chave.progresso = 0.00

        resultado_chave.save()

        # --- Parte 2: Atualizar o Objetivo Pai ---
        objetivo_pai = resultado_chave.objetivo
        
        media_progresso = objetivo_pai.resultados_chave.aggregate(
            media=Avg('progresso')
        ).get('media', 0.00)
        
        objetivo_pai.progresso = media_progresso if media_progresso is not None else 0.00
        objetivo_pai.save()

        # --- Parte 3: Salvar o Check-in associado ao usuário da requisição ---
        serializer.save(colaborador=self.request.user)