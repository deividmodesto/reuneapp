# reune_app/feedback/views.py

from rest_framework import viewsets
from .models import Feedback
from .serializers import FeedbackSerializer # <-- A linha que causa o erro

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint para enviar e visualizar feedbacks.
    """
    queryset = Feedback.objects.select_related('emissor', 'receptor').all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        # Quando tivermos segurança, o emissor será o usuário logado
        # serializer.save(emissor=self.request.user)
        
        # Solução temporária:
        from django.contrib.auth.models import User
        primeiro_usuario = User.objects.first()
        serializer.save(emissor=primeiro_usuario)