# reune_app/okr/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from avaliacoes.models import CicloAvaliacao # Importa o ciclo de outro app

# Modelo para os Objetivos
class Objetivo(models.Model):
    titulo = models.CharField(max_length=500, verbose_name="Título do Objetivo")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Responsável")
    # Um OKR pode estar atrelado a um ciclo de avaliação
    ciclo = models.ForeignKey(CicloAvaliacao, on_delete=models.CASCADE, verbose_name="Ciclo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    progresso = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Progresso (%)")

    
    class Meta:
        verbose_name = "Objetivo"
        verbose_name_plural = "Objetivos"
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo

# Modelo para os Resultados-Chave de um Objetivo
class ResultadoChave(models.Model):
    class TipoChoices(models.TextChoices):
        PERCENTUAL = 'Percentual', '%'
        FINANCEIRO = 'Financeiro', 'R$'
        NUMERICO = 'Numérico', 'Nº'

    objetivo = models.ForeignKey(Objetivo, related_name='resultados_chave', on_delete=models.CASCADE, verbose_name="Objetivo")
    descricao = models.CharField(max_length=500, verbose_name="Descrição do Resultado-Chave")
    tipo = models.CharField(max_length=50, choices=TipoChoices.choices, verbose_name="Tipo")
    valor_inicial = models.DecimalField(max_digits=18, decimal_places=2, default=0.0, verbose_name="Valor Inicial")
    valor_alvo = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Valor Alvo")
    progresso = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Progresso (%)")

    class Meta:
        verbose_name = "Resultado-Chave"
        verbose_name_plural = "Resultados-Chave"
        ordering = ['objetivo', 'id']

    def __str__(self):
        return self.descricao
    class Meta:
        verbose_name = "Resultado-Chave"
        verbose_name_plural = "Resultados-Chave"
        ordering = ['objetivo', 'id']

    def __str__(self):
        return self.descricao

# Modelo para os Check-ins de progresso de um Resultado-Chave
class CheckIn(models.Model):
    resultado_chave = models.ForeignKey(ResultadoChave, related_name='checkins', on_delete=models.CASCADE, verbose_name="Resultado-Chave")
    colaborador = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Colaborador")
    valor_atual = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Valor Atual do Check-in")
    nota_confianca = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Nota de Confiança",
        help_text="De 1 (em risco) a 5 (no caminho certo)"
    )
    comentario = models.TextField(verbose_name="Comentário")
    data_checkin = models.DateTimeField(auto_now_add=True, verbose_name="Data do Check-in")

    class Meta:
        verbose_name = "Check-in"
        verbose_name_plural = "Check-ins"
        ordering = ['-data_checkin']

    def __str__(self):
        return f"Check-in de {self.colaborador} em {self.data_checkin.strftime('%d/%m/%Y')}"