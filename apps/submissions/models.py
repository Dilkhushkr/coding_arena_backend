from django.db import models
from django.conf import settings
from apps.problems.models import Problem

class ProgrammingLanguage(models.Model):
    key = models.CharField(max_length=30, unique=True)
    display_name = models.CharField(max_length=50)
    file_extension = models.CharField(max_length=10)
    docker_image = models.CharField(max_length=100)
    compile_command = models.TextField(blank=True,null=True)
    run_command = models.TextField()

    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.display_name


class SubmissionStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    RUNNING = 'RUNNING', 'Running'
    ACCEPTED = 'ACCEPTED', 'Accepted'
    WRONG_ANSWER = 'WRONG_ANSWER', 'Wrong Answer'
    TIME_LIMIT_EXCEEDED = 'TIME_LIMIT_EXCEEDED', 'Time Limit Exceeded'
    COMPILATION_ERROR = 'COMPILATION_ERROR', 'Compilation Error'
    RUNTIME_ERROR = 'RUNTIME_ERROR', 'Runtime Error'
    INTERNAL_ERROR = 'INTERNAL_ERROR', 'Internal Error'


class Submission(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    problme = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
    )
    language = models.ForeignKey(
        ProgrammingLanguage,
        on_delete=models.PROTECT
    )

    code = models.TextField()

    result = models.CharField(
        max_length=20,
        choices = SubmissionStatus.choices,
        default=SubmissionStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} by {self.user}"
