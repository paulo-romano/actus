from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView

from actus.core.models import Problem


class ProblemListView(ListView):
    template_name = 'problem_list.html'
    model = Problem


class ProblemDetailView(DetailView):
    template_name = 'problem_detail.html'
    model = Problem


class ProblemUpdateView(UpdateView):
    template_name = 'problem_update.html'
    model = Problem
    fields = ['name',]