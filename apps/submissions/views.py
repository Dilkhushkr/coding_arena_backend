from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.problems.models import Problem
from .models import ProgrammingLanguage
from .serializers import ProgrammingLanguageSerializer
from .models import Submission



class ProgrammingLanguageListAPIView(APIView):
    def get(self,request):
        language = ProgrammingLanguage.objects.all()
        serializer = ProgrammingLanguageSerializer(language, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateSubmissionAPiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        problem_id = request.data.get('problem')
        language_id = request.data.get('language')
        code = request.data.get('code')

        if not all([problem_id,language_id,code]):
            return Response(
                {"error" : "All field are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return Response({
                "error": "Problem not found."
            },
            status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            language = ProgrammingLanguage.objects.get(id=language_id)
        except ProgrammingLanguage.DoesNotExist:
            return Response({
                "error": "Programming language not found."
            },
            status=status.HTTP_404_NOT_FOUND
            )
        
        submission = Submission.objects.create(
            user = request.user,
            problem = problem,
            language = language,
            code = code
        )

        return Response({
            'message' : 'Submission created successfully.',
            'submission_id' : submission.id,
             "status" : submission.result
        },
        status=status.HTTP_201_CREATED
        )
    


