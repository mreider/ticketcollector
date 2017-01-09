from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
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