from django.conf.urls import include, url

from .views import HomeView,LoginFailedView,DashboardView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='tickets'),
    url(r'^dashboard/$',DashboardView.as_view(),name='tickets_dashboard'),
    url(r'^login-error/$', LoginFailedView.as_view(),name='login_error'),
]