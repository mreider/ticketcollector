import json

from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import logout as auth_logout
from django.views.generic import DetailView
from django.views.generic import ListView
from zdesk import Zendesk
from zdesk import ZendeskError

from .models import Collection,Ticket,Comment, CollectionDocTicket
from .forms import CollectionCreateForm

class SearchHelper():
    def do_search(self,query):
        data = []
        zendesk = Zendesk(**settings.ZENDDESK_CONFIG)
        results = zendesk.search(query='type:ticket sort:desc ' + query)
        # print 'Results %s' % json.dumps(results)
        for item in results.get('results'):
            ticket_id = item.get('id')
            response = zendesk.user_show(id=item.get('requester_id')).get('user')
            requester = response.get('name') + ' ' + response.get('email')
            comments_response = zendesk.ticket_comments(ticket_id=ticket_id)
            ticket_item = TicketItem(name=item.get('subject'), id=ticket_id, created=item.get('created_at'),
                                   requester=requester,description=item.get('description'),
                                   is_public=item.get('is_public'))
            for cm in comments_response.get('comments'):
		print 'User Data %s'%posted_by_response
		name = posted_by_response.get('name') if posted_by_response.get('name') else cm.get('author_id')
		email = posted_by_response.get('email') if posted_by_response.get('email') else ''
  	        posted_by = name + ' ' + email

                #posted_by_response = zendesk.user_show(id=cm.get('author_id')).get('user')
                #posted_by = posted_by_response.get('name') + ' ' + posted_by_response.get('email')
                ticket_item.get_comments().append(TicketCommentItem(comment_id=cm.get('id'),ticket_id=ticket_id,
                                             is_public=cm.get('public'),comment=cm.get('plain_body'),
                                             posted_by=posted_by,created_at=cm.get('created_at')))

            data.append(ticket_item)
        return data

    def filter_duplicate(self,data):
        cleaned_data = []
        for x in data :
            if x not in cleaned_data:
                cleaned_data.append(x)
        return cleaned_data
    def search(self,search_query):
        data = []
        for single_query in search_query.split('[+]'):

            temp = self.do_search(query=single_query)
            for x in temp:
                data.append(x)
        filtered_data = self.filter_duplicate(data)
        return filtered_data

class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('new_collection'))
        else:
            return render(request, self.template_name)

class NewCollectionView(View):
    template_name = "new_collection.html"

    @method_decorator(login_required(login_url="/tickets/"))
    def get(self, request):
        return render(request, self.template_name)

class TicketCommentItem:
    def __init__(self,**kwargs):
        self.comment_id = kwargs.get('comment_id')
        self.ticket_id = kwargs.get('ticket_id')
        self.is_public = kwargs.get('is_public')
        self.comment = kwargs.get('comment')
        self.posted_by = kwargs.get('posted_by')
        self.created_at = datetime.strptime(kwargs.get('created_at'), '%Y-%m-%dT%H:%M:%SZ')
    def __eq__(self, other):
        return self.comment_id==other.comment_id

    def __hash__(self):
        return hash(('comment_id', self.comment_id))

class TicketItem:

    def add_comment(self,comment):
        self.comments.append(comment)
    def add_comments(self,comments):
        self.comments.extend(comments)

    def get_comments(self):
        return self.comments

    def __init__(self,**kwargs):
        self.ticket_name = kwargs.get('name')
        self.ticket_id = kwargs.get('id')

        self.created = datetime.strptime(kwargs.get('created'), '%Y-%m-%dT%H:%M:%SZ')
        self.requester = kwargs.get('requester')
        self.description = kwargs.get('description')
        self.is_public = kwargs.get('is_public')
        self.comments = []

    def __eq__(self, other):
        return self.ticket_id==other.ticket_id

    def __hash__(self):
        return hash(('ticket_id', self.ticket_id))

class CollectionSaveView(View):

    def save_seach_results(self,collection,search_results):

        for ticket_item in search_results:
            ticket = Ticket()
            ticket.collection = collection
            ticket.zd_ticket_id = ticket_item.ticket_id
            ticket.subject = ticket_item.ticket_name
            ticket.requester = ticket_item.requester
            ticket.description = ticket_item.description
            ticket.created_at = ticket_item.created
            ticket.save()
            for comment_item in ticket_item.get_comments():
                comment = Comment()
                comment.ticket = ticket
                comment.zd_comment_id = comment_item.comment_id
                comment.posted_by = comment_item.posted_by
                comment.created_at = comment_item.created_at
                comment.plain_body = comment_item.comment
                comment.is_public = comment_item.is_public
                comment.save()


    @method_decorator(login_required(login_url="/tickets/"))
    def post(self, request):
        # print request.POST
        form = CollectionCreateForm(request.POST)
        if form.is_valid():
            instance = form.save()
            filtered_data = SearchHelper().search(request.POST.get('search_criteria'))
            self.save_seach_results(instance,filtered_data)
            collection_id = instance.collection_id
            request.session['collection_id'] = collection_id
            return JsonResponse({"status":"Success",
                                 "message": "Collection name already exists.Choose another name.",
                                 "collection_id":instance.collection_id,
                                 "collection_name":instance.name})
        else:
            print form.errors
            return JsonResponse({"status":"Failed","error":"Collection name already exists.Choose another name."})


class TicketDetailsView(DetailView):
    template_name = "ticket_details_content.html"
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super(TicketDetailsView, self).get_context_data(**kwargs)
        return context

class CollectionDocView(DetailView):
    template_name = "collection_doc_view_modal_content.html"
    model = CollectionDocTicket

    def get_context_data(self, **kwargs):
        context = super(CollectionDocView, self).get_context_data(**kwargs)
        return context

class TicketSearchDetailsView(DetailView):
    template_name = "ticket_details_content.html"

    def get(self, request,ticket_id):
        context = {}
        ticket = Ticket.objects.filter(zd_ticket_id=ticket_id).first()
        context['object'] = ticket
        return render(request, self.template_name, context)


class CollectionDocDetailsView(View):
    template_name = 'collection_doc_details.html'

    @method_decorator(login_required(login_url="/tickets/"))
    def post(self,request,collection_id):
        ticket_id = request.POST.get('ticket')
        colletion = get_object_or_404(Collection,collection_id=collection_id)

        ticket = get_object_or_404(Ticket,ticket_id=ticket_id)
        colletion_doc,created = CollectionDocTicket.objects.get_or_create(collection=colletion)
        colletion_doc.collection = colletion
        colletion_doc.ticket.add(ticket)
        colletion_doc.save()
        return HttpResponseRedirect(reverse('collection-doc-details',kwargs={'collection_id':colletion.collection_id}))

    @method_decorator(login_required(login_url="/tickets/"))
    def get(self, request,collection_id):
        context = {}
        collection = get_object_or_404(Collection,collection_id=collection_id)
        context['collection'] = collection
        request.session['collection_id'] = collection.collection_id
        return render(request, self.template_name, context)

class CollectionDocFromSearchView(CollectionDocView):
    @method_decorator(login_required(login_url="/tickets/"))
    def post(self,request):
        ticket_id = request.POST.get('ticket')
        print(ticket_id)
        collection_id = request.POST.get('collection')
        colletion = get_object_or_404(Collection,collection_id=collection_id)
        ticket = Ticket.objects.filter(zd_ticket_id=ticket_id).first()
        colletion_doc,created = CollectionDocTicket.objects.get_or_create(collection=colletion)
        colletion_doc.collection = colletion
        colletion_doc.ticket.add(ticket)
        colletion_doc.save()
        return HttpResponseRedirect(reverse('collection-doc-details',kwargs={'collection_id':colletion.collection_id}))


class RemoveTicketFromDocView(View):
    @method_decorator(login_required(login_url="/tickets/"))
    def get(self, request,ticket_id,collection_doc_ticket_id):
        context = {}
        collection_doc = get_object_or_404(CollectionDocTicket,collection_doc_ticket_id=collection_doc_ticket_id)
        ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
        collection_doc.ticket.remove(ticket)
        collection_doc.save()
        context['collection'] = collection_doc.collection
        return HttpResponseRedirect(
            reverse('collection-doc-details', kwargs={'collection_id': collection_doc.collection.collection_id}))

class CollectionListView(ListView):
    model = Collection
    template_name = "collection_list.html"

    def get_context_data(self, **kwargs):
        context = super(CollectionListView, self).get_context_data(**kwargs)
        return context

class CollectionDeleteView(View):
    @method_decorator(login_required(login_url="/tickets/"))
    def get(self, request, id_obj):
        obj = get_object_or_404(Collection, collection_id=id_obj)
        obj.delete()
        message = 'Collection "{0}" successfully deleted.'.format(obj.name)
        messages.add_message(request, messages.SUCCESS, message)
        return redirect('list_collection')

class CollectionDetailsView(View):

    template_name = "collection_details.html"
    @method_decorator(login_required(login_url="/tickets/"))
    def get(self, request, id_obj):
        obj = get_object_or_404(Collection, collection_id=id_obj)
        try:
            collection_doc = CollectionDocTicket.objects.filter(collection=obj)
            return HttpResponseRedirect(reverse('collection-doc-details', kwargs={'collection_id': obj.collection_id}))
        except CollectionDocTicket.DoesNotExist:
            context = {}
            context['collection'] = obj
            return render(request, self.template_name, context)

class CollectionDocDownloadView(View):
    @method_decorator(login_required(login_url="/tickets/"))
    def get(self, request, pk):
        collection_doc = get_object_or_404(CollectionDocTicket, collection_doc_ticket_id=pk)
        line = ''
        for ticket in collection_doc.ticket.all():
            line = "Ticket # %s Request Date: %s \r"%(ticket.zd_ticket_id,ticket.created_at)
            line += "Subject : %s \r"%ticket.subject
            line += ticket.requester +"\r"
            for comment in ticket.comment_ticket.all():
            	if comment.is_public:
  		   line += " \t\t %s \r"%comment.created_at
		   line += " \t\t %s \r"%comment.posted_by
		   line += " \t\t %s \r"%comment.plain_body
            line += '----------------------------------------------\r'
        response = HttpResponse(line,content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="collection-doc.txt"'

        return response


class SearchResultsView(View):
    template_name = "search_results.html"
    def validate_search(self,search_query):
        delimiter = "[+]"
        if delimiter in search_query:
            print 'Delimiter in search'
            query = search_query.split(delimiter)
            print 'Number of segments in Query -->%s'%query
            is_valid = False
            for segment in query:
                if len(segment) > 0:
                    is_valid = True
                else:
                    is_valid = False
                    break
            return is_valid
        else:
            print 'Delimiter not in search'
            return True

    @method_decorator(login_required(login_url="/tickets/"))
    def get(self,request):
        search_query = request.GET.get('query')
        current_collection = request.GET.get('current-collection')

        context = {}
        context['query'] = search_query
        try:
            if not self.validate_search(search_query):
                print 'Query is not valid'
                messages.add_message(request, messages.ERROR, "Invalid search query. [+] is a delimiter.")
                return render(request, self.template_name, context)
            print 'Query is valid'
            filtered_data = SearchHelper().search(search_query)
            context['results'] = filtered_data
            context['search_count'] = len(filtered_data) if len(filtered_data) > 0 else 0
            if current_collection:
                collection = get_object_or_404(Collection,collection_id=current_collection)
                context['collection'] = collection
                render(request, 'collection_details.html', context)
            else:
                return render(request, self.template_name,context)
        except ZendeskError,e:
            print 'Error %s'%e.response.text
            messages.add_message(request, messages.ERROR, json.loads(e.response.text).get('error'))
            return render(request, self.template_name, context)


class DashboardView(View):
    template_name = 'dashboard.html'

    @method_decorator(login_required(login_url="/tickets/"))
    def get(self,request):
        # return render(request, self.template_name)
        return HttpResponseRedirect(reverse('new_collection'))

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