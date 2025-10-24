# reune_app/clima/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelo para o Termômetro de Humor diário
class RegistroHumor(models.Model):
    class HumorChoices(models.IntegerChoices):
        MUITO_TRISTE = 1, 'Muito Triste'
        TRISTE = 2, 'Triste'
        NEUTRO = 3, 'Neutro'
        FELIZ = 4, 'Feliz'
        MUITO_FELIZ = 5, 'Muito Feliz'

    colaborador = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Colaborador")
    data_registro = models.DateField(auto_now_add=True, verbose_name="Data do Registro")
    humor = models.IntegerField(choices=HumorChoices.choices, verbose_name="Humor")
    comentario = models.TextField(blank=True, null=True, verbose_name="Comentário")

    class Meta:
        verbose_name = "Registro de Humor"
        verbose_name_plural = "Registros de Humor"
        # Garante que cada colaborador só pode registrar o humor uma vez por dia
        unique_together = ('colaborador', 'data_registro')
        ordering = ['-data_registro']

    def __str__(self):
        return f"Humor de {self.colaborador.username} em {self.data_registro.strftime('%d/%m/%Y')}"