# reune_app/feedback/admin.py

from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('emissor', 'receptor', 'data_criacao')
    search_fields = ('emissor__username', 'receptor__username', 'texto')
    autocomplete_fields = ('emissor', 'receptor')