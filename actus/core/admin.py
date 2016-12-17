from django.contrib import admin
from actus.core.models import Problem, Comment, Category


class BaseModelAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at')


class CommentInlineAdmin(admin.TabularInline):
    model = Comment


@admin.register(Category)
class CategoryAdmin(BaseModelAdmin):
    short_description = 'Categorias'
    fields = ('name', )
    search_fields = ('name', )
    list_display = ('name', )


@admin.register(Problem)
class ProblemAdmin(BaseModelAdmin):
    short_description = 'Problemas'
    fields = ('name', 'category', 'created_by', 'description', 'duedate',
              'contributors', 'budget', 'budget_used', 'progress')
    search_fields = ('name', 'category', 'duedate',)
    list_display = ('name', 'created_by', 'duedate', 'budget',
                    'budget_used', 'progress')
    inlines = (CommentInlineAdmin,)
