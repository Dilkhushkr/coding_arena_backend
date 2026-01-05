from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Submission
from apps.problems.models import Problem
from .models import ProgrammingLanguage


class CreateSubmissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        problem_id = request.data.get('problem_id')
        code = request.data.get('code')
        language = request.data.get('language') 


        if not all ([problem_id,code,language]):
            return Response(
                {"error":"problem_id, code and language are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        problem = Problem.objects.get(id=problem_id)

        submission = Submission.objects.create(
            user = request.user,
            problem = problem,
            code = code,
            language = language
        )

        return Response(
            {
                "message": "Submission created",
                "submission_id": submission.id,
                "status": submission.result
            },
            status=status.HTTP_201_CREATED
        )