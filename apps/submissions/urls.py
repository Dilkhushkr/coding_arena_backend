from django.urls import path
from .views import CreateSubmissionView, ProgrammingLanguageListAPIView


urlpatterns = [
    # path('submit/', CreateSubmissionView.as_view(), name='create-submission'),
    path('programming-languages/', ProgrammingLanguageListAPIView.as_view(), name='programming-languages'),
]

