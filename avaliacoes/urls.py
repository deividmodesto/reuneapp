# reune_app/avaliacoes/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CicloAvaliacaoViewSet, CompetenciaViewSet, RespostaAvaliacaoViewSet

router = DefaultRouter()
router.register(r'ciclos', CicloAvaliacaoViewSet, basename='cicloavaliacao')
router.register(r'competencias', CompetenciaViewSet, basename='competencia')
router.register(r'respostas', RespostaAvaliacaoViewSet, basename='respostaavaliacao')

urlpatterns = [
    path('', include(router.urls)),
]