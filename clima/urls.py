# reune_app/clima/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroHumorViewSet

router = DefaultRouter()
router.register(r'registros-humor', RegistroHumorViewSet, basename='registrohumor')

urlpatterns = [
    path('', include(router.urls)),
]