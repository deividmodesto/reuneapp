# reune_app/okr/admin.py

from django.contrib import admin
from .models import Objetivo, ResultadoChave, CheckIn

class ResultadoChaveInline(admin.TabularInline):
    """
    Permite editar Resultados-Chave diretamente na página de um Objetivo.
    """
    model = ResultadoChave
    extra = 1 # Quantidade de campos extras para adicionar novos KRs

@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    """
    Configuração do painel Admin para Objetivos.
    """
    list_display = ('titulo', 'responsavel', 'ciclo')
    list_filter = ('ciclo', 'responsavel')
    search_fields = ('titulo', 'responsavel__first_name', 'responsavel__last_name')
    autocomplete_fields = ('responsavel', 'ciclo')
    inlines = [ResultadoChaveInline] # Adiciona a edição de KRs na mesma tela

# A CLASSE ABAIXO FOI ADICIONADA PARA CORRIGIR O ERRO
@admin.register(ResultadoChave)
class ResultadoChaveAdmin(admin.ModelAdmin):
    """
    Configuração do painel Admin para Resultados-Chave.
    """
    list_display = ('descricao', 'objetivo', 'tipo', 'valor_alvo')
    search_fields = ('descricao', 'objetivo__titulo') # Habilita a busca por descrição
    list_filter = ('tipo',)

@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    """
    Configuração do painel Admin para Check-ins.
    """
    list_display = ('resultado_chave', 'colaborador', 'valor_atual', 'nota_confianca', 'data_checkin')
    list_filter = ('nota_confianca', 'data_checkin')
    search_fields = ('resultado_chave__descricao', 'colaborador__first_name')
    autocomplete_fields = ('resultado_chave', 'colaborador')