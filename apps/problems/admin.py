from django.contrib import admin
from .models import Problem,TestCase


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'created_at')
    inlines = [TestCaseInline]
