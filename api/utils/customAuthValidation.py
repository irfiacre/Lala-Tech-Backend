from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from .utils import decodeJWT


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_token = request.COOKIES.get('access_token')
        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')        
        user = decodeJWT(user_token)

        return (user, None)