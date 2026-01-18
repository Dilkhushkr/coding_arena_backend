from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Problem
from .serializers import ProblemListSerializer, ProblemDetailSerializer


class ProblemListView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        problems = Problem.objects.all()
        seralizers = ProblemListSerializer(problems, many=True)
        return Response(seralizers.data, status=status.HTTP_200_OK)


class ProblemDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        problem = get_object_or_404(Problem, pk=pk)
        serializers = ProblemDetailSerializer(problem)
        return Response(serializers.data, status=status.HTTP_200_OK)

class ProblemDefficultyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, difficulty):
        difficulty = request.query_params.get('difficulty')
        problems = Problem.objects.all()
        if difficulty:
            problems = problems.filter(difficulty=difficulty)
        serializers = ProblemListSerializer(problems, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK) 