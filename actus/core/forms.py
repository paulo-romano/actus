from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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


class UserCreationForm(UserCreationForm):
    # def __init__(self, *args, **kwargs):
    #     super(UserCreateForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         self.fields['username'].widget.attrs['readonly'] = True
    #
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_active', 'date_joined')


class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'category', 'description', 'duedate', 'budget']

class CommetForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )