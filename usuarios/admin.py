# reune_app/usuarios/admin.py

from django.contrib import admin
from .models import Cargo, Equipe, Colaborador

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    """
    Configuração do painel Admin para o modelo Cargo.
    """
    list_display = ('titulo', 'id')
    search_fields = ('titulo',)

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    """
    Configuração do painel Admin para o modelo Equipe.
    """
    list_display = ('nome', 'lider')
    search_fields = ('nome',)
    autocomplete_fields = ('lider',) # Cria um campo de busca para selecionar o líder
    list_per_page = 20

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    """
    Configuração do painel Admin para o modelo Colaborador.
    """
    list_display = ('get_full_name', 'cargo', 'equipe', 'data_admissao')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'cargo__titulo', 'equipe__nome')
    list_filter = ('equipe', 'cargo', 'data_admissao')
    autocomplete_fields = ('usuario', 'cargo', 'equipe') # Facilita a busca para preencher os campos
    list_per_page = 25

    @admin.display(description='Nome do Colaborador', ordering='usuario__first_name')
    def get_full_name(self, obj):
        """
        Retorna o nome completo do usuário associado ao colaborador.
        """
        return obj.usuario.get_full_name() or obj.usuario.username