# reune_app/reune/urls.py

from django.contrib import admin
from django.urls import path, include
# IMPORTE AS VIEWS DE TOKEN
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- ROTAS DE AUTENTICAÇÃO ---
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # -----------------------------

    # APIs existentes
    path('api/usuarios/', include('usuarios.urls')),
    path('api/okr/', include('okr.urls')),
    path('api/avaliacoes/', include('avaliacoes.urls')),
    path('api/clima/', include('clima.urls')),
    path('api/feedback/', include('feedback.urls')),
]