import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import logout as auth_logout
from zdesk import Zendesk
from zdesk import ZendeskError


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('tickets_dashboard'))
        else:
            return render(request, self.template_name)

class NewCollectionView(View):
    template_name = "new_collection.html"

    @method_decorator(login_required(login_url="/tickets/"))
    def get(self, request):
        return render(request, self.template_name)

class TicketItem:
    def __init__(self,**kwargs):
        self.ticket_name = kwargs.get('name')
        self.ticket_id = kwargs.get('id')
        self.created = kwargs.get('created')
        self.requester = kwargs.get('requester')
    def __eq__(self, other):
        return self.ticket_id==other.ticket_id

    def __hash__(self):
        return hash(('ticket_id', self.ticket_id))

class SearchResultsView(View):
    template_name = "search_results.html"

    def do_search(self,query):
        data = []
        zendesk = Zendesk(**settings.ZENDDESK_CONFIG)
        results = zendesk.search(query='type:ticket sort:desc ' + query)
        print 'Results type %s' % results
        for item in results.get('results'):
            response = zendesk.user_show(id=item.get('requester_id')).get('user')
            # print 'USer Response %s'%response
            # print 'USer Response %s'%response.get('email')
            requester = response.get('name') + ' ' + response.get('email')
            data.append(TicketItem(name=item.get('subject'), id=item.get('id'), created=item.get('created_at'),
                                   requester=requester))
        return data

    def filter_duplicate(self,data):
        return list(set(data))

    @method_decorator(login_required(login_url="/tickets/"))
    def get(self,request):
        search_query = request.GET.get('query')

        context = {}
        context['query'] = search_query
        try:

            data = []
            for single_query in search_query.split('[+]'):
                data.extend(self.do_search(query=single_query))
            filtered_data = self.filter_duplicate(data)
            context['results'] = filtered_data
            context['search_count'] = len(filtered_data) if len(filtered_data) > 0 else 0
            return render(request, self.template_name,context)
        except ZendeskError,e:
            print 'Error %s'%e.response.text
            messages.add_message(request, messages.ERROR, json.loads(e.response.text).get('error'))
            return render(request, self.template_name, context)


class DashboardView(View):
    template_name = 'dashboard.html'

    @method_decorator(login_required(login_url="/tickets/"))
    def get(self,request):
        return render(request, self.template_name)


class LoginFailedView(View):
    template_name = 'login_error.html'
    def get(self,request):
        context = {}
        allowed_domain = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS[0]
        context['error_message'] = 'Only %s is allowed to login'%allowed_domain
        return render(request, self.template_name,context)

class LogoutView(View):
    def get(self,request):
        if request.user.is_authenticated():
            auth_logout(request)
        return HttpResponseRedirect(reverse('tickets'))