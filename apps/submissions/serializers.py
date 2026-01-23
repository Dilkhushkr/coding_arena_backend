from rest_framework import serializers
from .models import ProgrammingLanguage
from .models import Submission


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = ['id','display_name']

class SubmissionCreateSerializer(serializers.Serializer):
    class Meta:
        model = Submission
        fields = [
            "problem",
            "language",
            "code",
        ]
