from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.models import User
from django.template import RequestContext
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views.generic import ListView, DetailView, UpdateView, FormView, TemplateView
from actus.core.models import Problem, Comment
from actus.core.forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ProblemListView(LoginRequiredMixin, ListView):
    template_name = 'problem_list.html'
    model = Problem


class ProblemDetailView(DetailView):
    template_name = 'problem_detail.html'
    model = Problem

    def post(self, request, *args, **kwargs):
        Comment(created_by=request.user,
                problem=Problem.objects.get(pk=kwargs.get('pk')),
                body=request.POST.get('comment_body')).save()
        return redirect(resolve_url('problem-detail', *args, **kwargs))


class ProblemUpdateView(UpdateView):
    template_name = 'problem_update.html'
    model = Problem
    fields = ['name',]

def user_login(request):
    context = RequestContext(request)

    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.data.get('username'),
                                password=form.data.get('password'))
            if user and user.is_active:
                login(request, user)

                if is_safe_url(redirect_to):
                    return redirect(redirect_to)

                return redirect(resolve_url('home'))

    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'context': context})

def user_logout(request):
    logout(request)
    return redirect(resolve_url('login'))
