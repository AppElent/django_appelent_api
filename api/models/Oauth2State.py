from django.db import models
from django.contrib.auth import get_user_model
from crum import get_current_user
User = get_user_model()
from datetime import datetime, timedelta

def get_expires():
    return datetime.now()+timedelta(minutes=5)

class Oauth2State(models.Model):
    state = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_current_user)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def expired(self):
        expired_datetime = self.created_at+timedelta(minutes=5)
        if expired_datetime < datetime.now():
            return True
        #return self.expires_at < pendulum.now()
        return False