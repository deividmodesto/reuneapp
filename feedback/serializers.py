# reune_app/feedback/serializers.py

from rest_framework import serializers
from .models import Feedback
from usuarios.serializers import UserSerializer
from django.contrib.auth.models import User # <-- Verifique se este import existe

class FeedbackSerializer(serializers.ModelSerializer):
    emissor = UserSerializer(read_only=True)
    receptor = UserSerializer(read_only=True)

    receptor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='receptor', write_only=True
    )

    class Meta:
        model = Feedback
        fields = [
            'id',
            'emissor',
            'receptor',
            'receptor_id',
            'texto',
            'data_criacao'
        ]