from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import BaseAuthentication

from .utils import verify_firebase_token


class FirebaseUser:
    def __init__(self, uid):
        self.uid = uid
        self.is_authenticated = True

    def __str__(self):
        return f"FirebaseUser {self.uid}"


class FirebaseAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def get_authorization_header(self, request):
        """
        Return request's 'Authorization:' header, as a bytestring.

        Hide some test client ickyness where the header can be unicode.
        """

        auth = request.META.get("HTTP_AUTHORIZATION", b"")
        if isinstance(auth, str):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def authenticate(self, request):
        auth = self.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            return None
        elif len(auth) > 2:
            return None

        try:
            token = auth[1].decode()
        except UnicodeError:
            return None

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        uid = verify_firebase_token(key)
        if uid is None:
            return None

        user = FirebaseUser(uid)
        return (user, None)
