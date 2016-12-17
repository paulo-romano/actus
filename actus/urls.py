from django.conf.urls import url, include
from django.contrib import admin
from actus.core.views import (ProblemListView, ProblemDetailView,
                              ProblemUpdateView, user_login, user_logout,
                              UserUpdateView, ProblemCreateView,
                              problem_collaborate, UserCreateView,
                              problem_invite)
import notifications.urls

urlpatterns = [
    url(r'^$', ProblemListView.as_view(), name='home'),
    url(r'^problem/create/$', ProblemCreateView.as_view(success_url='/'),
        name='problem-create'),
    url(r'^problem/(?P<pk>[^/]+)/$', ProblemDetailView.as_view(),
        name='problem-detail'),
    url(r'^problem/(?P<pk>[^/]+)/update/$',
        ProblemUpdateView.as_view(success_url='/'), name='problem-update'),
    url(r'^problem/(?P<pk>[^/]+)/collaborate/$', problem_collaborate,
        name='problem-collaborate'),
    url(r'^problem/(?P<pk>[^/]+)/invite/$', problem_invite,
        name='problem-invite'),

    url(r'^accounts/login/$', user_login, name='login'),
    url(r'^accounts/logout/$', user_logout, name='logout'),
    url(r'^accounts/(?P<pk>[^/]+)/update/$',
        UserUpdateView.as_view(success_url='/'), name='user-update'),
    url(r'^accounts/create/$', UserCreateView.as_view(success_url='/'),
        name='user-create'),

    url(r'^admin/', admin.site.urls),
    url('^inbox/notifications/', include(notifications.urls,
                                         namespace='notifications')),
]
