from django.shortcuts import render
from django.views.generic import ListView

from actus.core.models import Problem


class ProblemListView(ListView):
    template_name = 'problem_list.html'
    model = Problem
