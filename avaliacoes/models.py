# reune_app/avaliacoes/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelo para os ciclos de avaliação (ex: "Avaliação Semestral 2025.1")
class CicloAvaliacao(models.Model):
    class StatusChoices(models.TextChoices):
        PLANEJAMENTO = 'Planejamento', 'Planejamento'
        ATIVO = 'Ativo', 'Ativo'
        CONCLUIDO = 'Concluído', 'Concluído'

    titulo = models.CharField(max_length=255, verbose_name="Título do Ciclo")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Fim")
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.PLANEJAMENTO, verbose_name="Status")

    class Meta:
        verbose_name = "Ciclo de Avaliação"
        verbose_name_plural = "Ciclos de Avaliação"
        ordering = ['-data_inicio']

    def __str__(self):
        return self.titulo

# Modelo para as competências que serão avaliadas
class Competencia(models.Model):
    nome = models.CharField(max_length=255, unique=True, verbose_name="Nome da Competência")
    descricao = models.TextField(verbose_name="Descrição")

    class Meta:
        verbose_name = "Competência"
        verbose_name_plural = "Competências"
        ordering = ['nome']

    def __str__(self):
        return self.nome

# Armazena cada resposta individual de uma avaliação
class RespostaAvaliacao(models.Model):
    ciclo = models.ForeignKey(CicloAvaliacao, on_delete=models.CASCADE, verbose_name="Ciclo")
    avaliado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes_recebidas', verbose_name="Avaliado")
    avaliador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes_feitas', verbose_name="Avaliador")
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE, verbose_name="Competência")
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Nota",
        help_text="Nota de 1 a 5"
    )
    justificativa = models.TextField(blank=True, null=True, verbose_name="Justificativa")
    data_resposta = models.DateTimeField(auto_now_add=True, verbose_name="Data da Resposta")

    class Meta:
        verbose_name = "Resposta de Avaliação"
        verbose_name_plural = "Respostas de Avaliação"
        # Garante que um avaliador só pode avaliar uma competência de um avaliado uma vez por ciclo
        unique_together = ('ciclo', 'avaliado', 'avaliador', 'competencia')

    def __str__(self):
        return f"Avaliação de {self.avaliado} por {self.avaliador} - {self.competencia.nome}"