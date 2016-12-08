from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.models import User
from django.template import RequestContext
from django.urls import reverse
from django.utils.http import is_safe_url
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView, UpdateView, FormView, TemplateView
from actus.core.models import Problem, Comment
from actus.core.forms import LoginForm, ProblemForm, ProfileForm, CommetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from notifications.models import Notification


def get_context_notifications(user):
    return Notification.objects.filter(recipient=user)


class ProblemListView(LoginRequiredMixin, ListView):
    template_name = 'problem_list.html'
    model = Problem

    def get_context_data(self, **kwargs):
        ctx = super(ProblemListView, self).get_context_data(**kwargs)
        ctx['total_contributors'] = User.objects.count()
        ctx['total_problems'] = Problem.objects.count()
        ctx['total_open_problems'] = len(Problem.objects.filter(progress__lte=99.9))
        ctx['total_open_problems_perc'] = round((ctx['total_open_problems'] / ctx['total_problems']) * 100, 2)
        ctx['total_closed_problems'] = len(Problem.objects.filter(progress__gte=100))
        ctx['total_closed_problems_perc'] = round((ctx['total_closed_problems'] / ctx['total_problems']) * 100, 2)
        ctx['total_comments'] = Comment.objects.count()
        ctx['notifications'] = get_context_notifications(self.request.user)
        ctx['notifications_qty'] = len(ctx['notifications'])

        total_donated_value = 0
        for p in Problem.objects.all():
            total_donated_value += p.budget_used

        ctx['total_donated_value'] = total_donated_value
        return ctx


class ProblemDetailView(DetailView):
    template_name = 'problem_detail.html'
    model = Problem

    def get_context_data(self, **kwargs):
        ctx = super(ProblemDetailView, self).get_context_data(**kwargs)
        ctx['notifications'] = get_context_notifications(self.request.user)
        ctx['notifications_qty'] = len(ctx['notifications'])
        return ctx

    def post(self, request, *args, **kwargs):
        problem = Problem.objects.get(pk=kwargs.get('pk'))
        body = request.POST.get('comment_body')

        if request.POST.get('budget_used'):
            problem.budget_used = request.POST.get('budget_used')
            problem.save()
            if body:
                body += '<br/><br/>'

            body += '==> Gasto: R$ ' + str(problem.budget_used)

        if request.POST.get('progress'):
            problem.progress = request.POST.get('progress')
            problem.save()

            if not '<br/><br/>' in body:
                body += '<br/>'

            body += '<br/>' + '==> Progresso: ' + str(problem.progress) + '%'

        Comment(created_by=request.user,
                problem=problem,
                body=body).save()
        return redirect(resolve_url('problem-detail', *args, **kwargs))


class ProblemUpdateView(UpdateView):
    template_name = 'problem_update.html'
    model = Problem
    form_class = ProblemForm

    def get_context_data(self, **kwargs):
        ctx = super(ProblemUpdateView, self).get_context_data(**kwargs)
        ctx['notifications'] = get_context_notifications(self.request.user)
        ctx['notifications_qty'] = len(ctx['notifications'])
        return ctx

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super(ProblemUpdateView, self).form_valid(form)


class ProblemCreateView(CreateView):
    template_name = 'problem_create.html'
    model = Problem
    form_class = ProblemForm

    def get_context_data(self, **kwargs):
        ctx = super(ProblemCreateView, self).get_context_data(**kwargs)
        ctx['notifications'] = get_context_notifications(self.request.user)
        ctx['notifications_qty'] = len(ctx['notifications'])
        return ctx

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super(ProblemCreateView, self).form_valid(form)


class UserUpdateView(UpdateView):
    template_name = 'user_update.html'
    model = User
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        ctx = super(UserUpdateView, self).get_context_data(**kwargs)
        ctx['notifications'] = get_context_notifications(self.request.user)
        ctx['notifications_qty'] = len(ctx['notifications'])
        return ctx

def problem_collaborate(request, pk):
    context = RequestContext(request)
    problem = Problem.objects.get(pk=pk)

    if request.method == 'POST':
        form = CommetForm(data=request.POST)
        if form.is_valid():
            problem.contributors.add(request.user)
            Comment.objects.create(created_by=request.user,
                                   updated_by=request.user,
                                   problem=problem,
                                   body=form.data.get('body'))

            return redirect('problem-detail', pk=pk)
    else:
        form = CommetForm()

    return render(request, 'problem_collaborate.html',
                  {'form': form, 'context': context, 'problem': problem})

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
