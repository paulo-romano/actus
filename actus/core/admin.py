from django.contrib import admin

from actus.core.models import Problem, Comment

class BaseModelAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at')


class CommentInlineAdmin(admin.TabularInline):
    model = Comment

@admin.register(Problem)
class ProblemAdmin(BaseModelAdmin):
    short_description = 'Problemas'
    fields = ('name', 'created_by', 'description', 'duedate', 'budget', 'budget_used')
    search_fields = ('name', 'duedate',)
    list_display = ('name', 'created_by', 'duedate', 'budget', 'budget_used')
    inlines = (CommentInlineAdmin,)

