
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import logout as auth_logout


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('tickets_dashboard'))
        else:
            return render(request, self.template_name)

class DashboardView(View):
    template_name = 'dashboard.html'

    @method_decorator(login_required())
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