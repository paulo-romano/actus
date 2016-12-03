from django.contrib import admin

from actus.core.models import Problem

class BaseModelAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'created_by', 'updated_at', 'updated_by')


@admin.register(Problem)
class ProblemAdmin(BaseModelAdmin):
    short_description = 'Problemas'
    fields = ('name', 'description', 'duedate',)
    search_fields = ('name', 'duedate',)
    list_display = ('name', 'duedate',)

