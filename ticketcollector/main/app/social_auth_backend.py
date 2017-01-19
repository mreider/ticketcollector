import json
from urllib import urlencode

from django.conf import settings
from social.backends.oauth import BaseOAuth2

class ZenDeskOAuth2(BaseOAuth2):
    """Github OAuth authentication backend"""
    name = 'zendesk'
    ZEN_DESK_URL = settings.ZENDDESK_CONFIG.get('zdesk_url')
    AUTHORIZATION_URL = ZEN_DESK_URL+'/oauth/authorizations/new'
    ACCESS_TOKEN_URL = ZEN_DESK_URL+'/oauth/tokens'
    PROFILE_URL = ZEN_DESK_URL+'/api/v2/users/me.json'
    DEFAULT_SCOPE = 'read'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Github account"""
        return {'username': response.get('user').get('email'),
                'email': response.get('user').get('email') or '',
                'first_name': response.get('user').get('name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        bearer_token = 'Bearer ' + access_token
        header = {'Authorization': bearer_token}
        # url = 'https://api.github.com/user?' + urlencode({
        #     'access_token': access_token
        # })
        try:
            # request = urllib2.Request("http://www.google.com", headers={"Accept": "text/html"})
            return json.load(self.request(self.PROFILE_URL,headers=header))
        except ValueError:
            return None

class GithubOAuth2(BaseOAuth2):
    """Github OAuth authentication backend"""
    name = 'github'
    AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Github account"""
        return {'username': response.get('login'),
                'email': response.get('email') or '',
                'first_name': response.get('name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.github.com/user?' + urlencode({
            'access_token': access_token
        })
        try:
            return json.load(self.urlopen(url))
        except ValueError:
            return None