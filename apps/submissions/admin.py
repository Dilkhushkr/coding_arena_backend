from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'language', 'result', 'created_at')
    list_filter = ('language', 'result')
