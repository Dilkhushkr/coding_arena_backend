from django.urls import path
from .views import CreateSubmissionAPiView, ProgrammingLanguageListAPIView


urlpatterns = [
    path('submit/', CreateSubmissionAPiView.as_view(), name='create-submission'),
    path('programming-languages/', ProgrammingLanguageListAPIView.as_view(), name='programming-languages'),
]

