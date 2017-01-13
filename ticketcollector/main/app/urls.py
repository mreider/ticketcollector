from django.conf.urls import include, url

from .views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='tickets'),
    url(r'^dashboard/$',DashboardView.as_view(),name='tickets_dashboard'),
    url(r'^new_collection/$',NewCollectionView.as_view(),name='new_collection'),
    url(r'^save_collection/$',CollectionSaveView.as_view(),name='save_collection'),
    url(r'^list_collection/$',CollectionListView.as_view(),name='list_collection'),
    url(r'^delete_collection/(?P<id_obj>[\w-]+)/$',CollectionDeleteView.as_view(),name='delete_collection'),
    url(r'^open_collection/(?P<id_obj>[\w-]+)/$', CollectionDetailsView.as_view(), name='open_collection'),
    url(r'^search_results/$', SearchResultsView.as_view(), name='search_results'),
    url(r'^login-error/$', LoginFailedView.as_view(),name='login_error'),
    url(r'^logout/$', LogoutView.as_view(),name='logout'),
    url(r'^details/(?P<pk>[\w-]+)/$', TicketDetailsView.as_view(), name='ticket-detail'),
    url(r'^details_search/(?P<ticket_id>[\w-]+)/$', TicketSearchDetailsView.as_view(), name='ticket-detail-search'),
]