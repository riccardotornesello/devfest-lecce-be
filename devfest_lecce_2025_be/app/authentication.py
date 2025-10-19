"""
Firebase Authentication for Django REST Framework.

This module provides a custom authentication backend that integrates Firebase
authentication with Django REST Framework. It validates Firebase ID tokens
and creates FirebaseUser objects for authenticated requests.
"""

from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import BaseAuthentication

from .utils import verify_firebase_token


class FirebaseUser:
    """
    Represents a Firebase-authenticated user.

    This lightweight user class is used instead of Django's built-in User model
    since Firebase handles user management externally.

    Attributes:
        uid (str): The Firebase user ID
        is_authenticated (bool): Always True for valid FirebaseUser instances
    """

    def __init__(self, uid):
        self.uid = uid
        self.is_authenticated = True

    def __str__(self):
        return f"FirebaseUser {self.uid}"


class FirebaseAuthentication(BaseAuthentication):
    """
    Custom authentication backend for Firebase ID tokens.

    This class validates Bearer tokens from the Authorization header against
    Firebase's authentication service. Valid tokens result in a FirebaseUser
    being attached to the request.

    Usage:
        Add to REST_FRAMEWORK settings:

        REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'app.authentication.FirebaseAuthentication',
            ],
        }
    """

    keyword = "Bearer"

    def get_authorization_header(self, request):
        """
        Extract and return the Authorization header from the request.

        Args:
            request: The HTTP request object

        Returns:
            bytes: The Authorization header value as bytes
        """

        auth = request.META.get("HTTP_AUTHORIZATION", b"")
        if isinstance(auth, str):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def authenticate(self, request):
        """
        Authenticate the request using the Firebase ID token.

        Args:
            request: The HTTP request object

        Returns:
            tuple: (FirebaseUser, None) if authentication succeeds
            None: If authentication fails or no token is present
        """
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
        """
        Validate the Firebase token and return a FirebaseUser.

        Args:
            key (str): The Firebase ID token to validate

        Returns:
            tuple: (FirebaseUser, None) if validation succeeds
            None: If validation fails
        """
        uid = verify_firebase_token(key)
        if uid is None:
            return None

        user = FirebaseUser(uid)
        return (user, None)
