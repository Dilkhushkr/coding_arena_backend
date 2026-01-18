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



