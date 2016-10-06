from django.shortcuts import render
from django.views.generic import ListView

from actus.core.models import Problem


class HomeView(ListView):
    template_name = 'home.html'
    model = Problem
