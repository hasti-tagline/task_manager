from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .utils import decrypt_api_key


class APIKeyAuthentication(BaseAuthentication):

    def authenticate(self, request):

        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return None

        for u in User.objects.all():

            try:
                if decrypt_api_key(u.api_key) == api_key:
                    user = u
                    break

            except Exception:
                continue

        if not user:
            raise AuthenticationFailed(
                "Invalid API Key"
            )

        if user.role not in ["admin", "manager"]:
            raise AuthenticationFailed(
                "Only admin and managers can use API Keys"
            )

        return (user, None) 
    


    