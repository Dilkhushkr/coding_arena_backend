from django.contrib import admin
from .models import ProgrammingLanguage

@admin.register(ProgrammingLanguage)

class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
        'key',
        'file_extension',
        'docker_image',
        'is_active',
    )
    list_filter = ('is_active',)
    search_fields = ('display_name', 'key')
    ordering = ('display_name',)

    readonly_fields = ()