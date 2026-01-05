from django.urls import path
from .views import CreateSubmissionView


urlpatterns = [
    path('submit/', CreateSubmissionView.as_view(), name='create-submission'),
]

