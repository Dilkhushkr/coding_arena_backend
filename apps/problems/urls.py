from django.urls import path
from .views import ProblemListView, ProblemDetailView,ProblemDefficultyView

urlpatterns = [
    path("", ProblemListView.as_view(), name="problem-list"),
    path("<int:pk>/", ProblemDetailView.as_view(), name="problem-detail"),
    path("difficulty/<str:difficulty>/", ProblemDefficultyView.as_view(), name="problem-difficulty"),
]
