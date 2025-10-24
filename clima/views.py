# reune_app/clima/views.py

from rest_framework import viewsets
from .models import RegistroHumor
from .serializers import RegistroHumorSerializer

class RegistroHumorViewSet(viewsets.ModelViewSet):
    """
    API endpoint para visualizar e registrar o humor dos colaboradores.
    """
    queryset = RegistroHumor.objects.select_related('colaborador').all()
    serializer_class = RegistroHumorSerializer

    # Futuramente, quando tivermos autenticação, o colaborador
    # será pego automaticamente do usuário que fez a requisição.
    # def perform_create(self, serializer):
    #     serializer.save(colaborador=self.request.user)