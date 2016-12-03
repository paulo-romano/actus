from django.db import models

class BaseModel(models.Model):
    from uuid import uuid4
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Problem(BaseModel):
    name = models.CharField(verbose_name='Nome', max_length=100)
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    duedate = models.DateField(verbose_name='Data Finalização')

    class Meta:
        verbose_name = 'problema'
        verbose_name_plural = 'problemas'