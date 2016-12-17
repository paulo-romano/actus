from django.db import models
from django.contrib.auth.models import User
from notifications.signals import notify
from django.dispatch import receiver

class BaseModel(models.Model):
    from uuid import uuid4
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        User, verbose_name='Criador',
        related_name='%(app_label)s_%(class)s_created_by', null=True,
        blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(
        User, verbose_name='Alterador por',
        related_name='%(app_label)s_%(class)s_updated_by',
        null=True, blank=True)

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
    description = models.TextField(verbose_name='Descrição', null=True,
                                   blank=True)
    category = models.ForeignKey(Category, verbose_name='Categoria',
                                 null=True, blank=True)
    duedate = models.DateField(verbose_name='Data Finalização')
    budget = models.DecimalField(verbose_name='Orçamento',
                                 decimal_places=2, max_digits=10,
                                 default=0)
    budget_used = models.DecimalField(verbose_name='Gasto',
                                      decimal_places=2, max_digits=10,
                                      default=0)
    progress = models.DecimalField(verbose_name='Gasto', decimal_places=2,
                                   max_digits=10, default=0)
    contributors = models.ManyToManyField(User,
                                          verbose_name='Colaboradores')

    def __str__(self):
        return self.name

    @staticmethod
    @receiver(models.signals.post_save, sender='core.Problem')
    def post_save(sender, instance, created, **kwargs):
        if created:
            instance.contributors.add(instance.created_by)

        for user in User.objects.all():
            verb = 'Criou' if created else 'Editou'
            notify.send(instance.created_by, target=instance,
                        recipient=user, verb=verb + ' o problema ' +
                        instance.name)

    class Meta:
        verbose_name = 'problema'
        verbose_name_plural = 'problemas'


class Comment(BaseModel):
    problem = models.ForeignKey(Problem)
    body = models.TextField(verbose_name='Comentário', null=True,
                            blank=True)

    def __str__(self):
        return self.created_by.first_name + ' comentou em ' + str(
               self.created_at)

    @staticmethod
    @receiver(models.signals.post_save, sender='core.Comment')
    def post_save(sender, instance, created, **kwargs):
        if created:
            for user in instance.problem.contributors.all():
                notify.send(instance.created_by, target=instance.problem,
                            recipient=user,
                            verb='Comentou no problema ' +
                            instance.problem.name)
                if float(instance.problem.progress) >= 100:
                    notify.send(instance.created_by,
                                target=instance.problem, recipient=user,
                                verb='O problema {0} foi resolvido!'
                                .format(instance.problem.name))

    class Meta:
        verbose_name = 'problema'
        verbose_name_plural = 'problemas'
