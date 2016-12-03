from django.contrib import admin

from actus.core.models import Problem, Comment

class BaseModelAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'created_by', 'updated_at', 'updated_by')


class CommentInlineAdmin(admin.TabularInline):
    model = Comment

@admin.register(Problem)
class ProblemAdmin(BaseModelAdmin):
    short_description = 'Problemas'
    fields = ('name', 'description', 'duedate', 'budget', 'budget_used')
    search_fields = ('name', 'duedate',)
    list_display = ('name', 'duedate', 'budget', 'budget_used')
    inlines = (CommentInlineAdmin,)

