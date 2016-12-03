from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm

from actus.core.models import Problem


class LoginForm(AuthenticationForm):
    pass


class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'description', 'duedate', 'budget']