from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CargoViewSet, EquipeViewSet, ColaboradorViewSet

# Cria um roteador para registrar as ViewSets
router = DefaultRouter()
router.register(r'cargos', CargoViewSet, basename='cargo')
router.register(r'equipes', EquipeViewSet, basename='equipe')
router.register(r'colaboradores', ColaboradorViewSet, basename='colaborador')

# As URLs da API são determinadas automaticamente pelo roteador
urlpatterns = [
    path('', include(router.urls)),
]