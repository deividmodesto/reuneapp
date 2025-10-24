# reune_app/okr/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObjetivoViewSet, ResultadoChaveViewSet, CheckInViewSet

router = DefaultRouter()
router.register(r'objetivos', ObjetivoViewSet, basename='objetivo')
router.register(r'resultados-chave', ResultadoChaveViewSet, basename='resultadochave')
router.register(r'checkins', CheckInViewSet, basename='checkin')

urlpatterns = [
    path('', include(router.urls)),
]