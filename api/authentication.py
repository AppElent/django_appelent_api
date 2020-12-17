from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model
User = get_user_model()
import firebase_admin
from firebase_admin import credentials, auth
import os
import json 

cred = credentials.Certificate(json.loads(os.getenv("FIREBASE_CRED")))
firebase_admin.initialize_app(cred)
print('Firebase loaded')

class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Authentication for firebase front-ends.
    Needs Authorization header in the form of "Firebase <token>" to work.
    """
    def authenticate(self, request, **credentials):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None

        if not token.startswith("Firebase"):
            return None

        token = token.replace("Firebase ", "")
     
        try:
            decoded = auth.verify_id_token(token)
        except:
            raise exceptions.AuthenticationFailed('Token incorrect')
        
        try:
            user = User.objects.get(email=decoded["email"])
            if user.firebase_uid is None:
                user.firebase_uid = decoded["uid"]
                user.save()
        except User.DoesNotExist:
            try:
                user = User.objects.create_user(email=decoded["email"])
            except:
                raise exceptions.AuthenticationFailed('User does not exist and cannot be created')

        return (user, None)