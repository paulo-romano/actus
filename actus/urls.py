"""actus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from actus.core.views import ProblemListView, ProblemDetailView, ProblemUpdateView, user_login, user_logout
from django.urls import reverse

urlpatterns = [
    url(r'^$', ProblemListView.as_view(), name='home'),
    url(r'^problem/(?P<pk>[^/]+)/$', ProblemDetailView.as_view(), name='problem-detail'),
    url(r'^problem/(?P<pk>[^/]+)/update/$', ProblemUpdateView.as_view(success_url='/'), name='problem-update'),

    url(r'^accounts/login/$', user_login, name='login'),
    url(r'^accounts/logout/$', user_logout, name='logout'),
    url(r'^admin/', admin.site.urls),
]
