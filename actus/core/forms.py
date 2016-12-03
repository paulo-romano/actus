from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm

from actus.core.models import Problem, Comment


class LoginForm(AuthenticationForm):
    pass


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'description', 'duedate', 'budget']

class CommetForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )