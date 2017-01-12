from django.conf.urls import include, url

from .views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='tickets'),
    url(r'^dashboard/$',DashboardView.as_view(),name='tickets_dashboard'),
    url(r'^new_collection/$',NewCollectionView.as_view(),name='new_collection'),
    url(r'^save_collection/$',CollectionSaveView.as_view(),name='save_collection'),
    url(r'^search_results/$', SearchResultsView.as_view(), name='search_results'),
    url(r'^login-error/$', LoginFailedView.as_view(),name='login_error'),
    url(r'^logout/$', LogoutView.as_view(),name='logout'),
]