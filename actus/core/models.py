from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    from uuid import uuid4
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, verbose_name='Criador', related_name='%(app_label)s_%(class)s_created_by', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(User, verbose_name='Alterador por', related_name='%(app_label)s_%(class)s_updated_by', null=True, blank=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(verbose_name='Nome', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

class Problem(BaseModel):
    name = models.CharField(verbose_name='Nome', max_length=100)
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name='Categoria', null=True, blank=True)
    duedate = models.DateField(verbose_name='Data Finalização')
    budget = models.DecimalField(verbose_name='Orçamento', decimal_places=2, max_digits=10, default=0)
    budget_used = models.DecimalField(verbose_name='Gasto', decimal_places=2, max_digits=10, default=0)
    progress = models.DecimalField(verbose_name='Gasto', decimal_places=2, max_digits=10, default=0)
    contributors = models.ManyToManyField(User, verbose_name='Colaboradores')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'problema'
        verbose_name_plural = 'problemas'


class Comment(BaseModel):
    problem = models.ForeignKey(Problem)
    body = models.TextField(verbose_name='Comentário', null=True, blank=True)

    def __str__(self):
        return self.created_by.first_name + ' comentou em ' + str(self.created_at)

    class Meta:
        verbose_name = 'problema'
        verbose_name_plural = 'problemas'