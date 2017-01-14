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
    url(r'^collection_doc_details/(?P<collection_id>[\w-]+)/$', CollectionDocDetailsView.as_view(), name='collection-doc-details'),
    url(r'^collection-doc-details-search/$', CollectionDocFromSearchView.as_view(), name='collection-doc-details-search'),
    url(r'^view_collection_doc_details/(?P<pk>[\w-]+)/$',CollectionDocView.as_view() , name='view-collection-doc-details'),
    url(r'^collection_doc_details_remove_ticket/(?P<ticket_id>[\w-]+)/(?P<collection_doc_ticket_id>[\w-]+)/$', RemoveTicketFromDocView.as_view(), name='remove-ticket-doc'),
    url(r'^download_collection_doc_details/(?P<pk>[\w-]+)/$', CollectionDocDownloadView.as_view(),name='download-collection-doc'),

]