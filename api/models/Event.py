from django.db import models
from django.contrib.auth import get_user_model
from crum import get_current_user
User = get_user_model()

class Event(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_current_user)
    application = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    severity = models.IntegerField()
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.application + " - " + str(self.severity) + " - " + self.value 