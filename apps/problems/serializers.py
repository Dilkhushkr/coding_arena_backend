from rest_framework import serializers
from .models import Problem


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'title', 'difficulty', 'time_limit', 'created_at']

class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = "__all__"