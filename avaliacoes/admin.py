# reune_app/avaliacoes/admin.py

from django.contrib import admin
from .models import CicloAvaliacao, Competencia, RespostaAvaliacao

@admin.register(CicloAvaliacao)
class CicloAvaliacaoAdmin(admin.ModelAdmin):
    """
    Configuração do painel Admin para Ciclos de Avaliação.
    """
    list_display = ('titulo', 'data_inicio', 'data_fim', 'status')
    list_filter = ('status',)
    search_fields = ('titulo',)

@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    """
    Configuração do painel Admin para Competências.
    """
    list_display = ('nome', 'id')
    search_fields = ('nome',)

@admin.register(RespostaAvaliacao)
class RespostaAvaliacaoAdmin(admin.ModelAdmin):
    """
    Configuração do painel Admin para Respostas de Avaliação.
    """
    list_display = ('get_avaliado_name', 'get_avaliador_name', 'competencia', 'nota', 'ciclo')
    list_filter = ('ciclo', 'competencia', 'nota')
    search_fields = ('avaliado__first_name', 'avaliado__last_name', 'avaliador__first_name', 'avaliador__last_name', 'competencia__nome')
    autocomplete_fields = ('avaliado', 'avaliador', 'competencia', 'ciclo')
    list_per_page = 30

    @admin.display(description='Avaliado', ordering='avaliado__first_name')
    def get_avaliado_name(self, obj):
        return obj.avaliado.get_full_name() or obj.avaliado.username

    @admin.display(description='Avaliador', ordering='avaliador__first_name')
    def get_avaliador_name(self, obj):
        return obj.avaliador.get_full_name() or obj.avaliador.username