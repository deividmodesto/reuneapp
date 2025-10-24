# reune_app/clima/admin.py

from django.contrib import admin
from .models import RegistroHumor

@admin.register(RegistroHumor)
class RegistroHumorAdmin(admin.ModelAdmin):
    """
    Configuração do painel Admin para Registros de Humor.
    """
    list_display = ('get_colaborador_name', 'data_registro', 'get_humor_display')
    list_filter = ('humor', 'data_registro')
    search_fields = ('colaborador__first_name', 'colaborador__last_name')
    autocomplete_fields = ('colaborador',)
    date_hierarchy = 'data_registro'

    @admin.display(description='Colaborador', ordering='colaborador__first_name')
    def get_colaborador_name(self, obj):
        return obj.colaborador.get_full_name() or obj.colaborador.username

    # A linha que causava o erro foi removida daqui.
    # O título da coluna 'Humor' já é definido automaticamente pelo verbose_name no models.py