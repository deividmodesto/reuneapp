# reune_app/feedback/models.py

from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    emissor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_enviados', verbose_name="Emissor")
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_recebidos', verbose_name="Receptor")
    texto = models.TextField(verbose_name="Conteúdo do Feedback")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Feedback de {self.emissor.username} para {self.receptor.username} em {self.data_criacao.strftime('%d/%m/%Y')}"