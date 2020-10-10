from django.db import models
from django.contrib.auth import get_user_model
from crum import get_current_user
User = get_user_model()

class Meterstand(models.Model):
    kwh_180 = models.IntegerField()
    kwh_181 = models.IntegerField()
    kwh_182 = models.IntegerField()
    kwh_280 = models.IntegerField()
    kwh_281 = models.IntegerField()
    kwh_282 = models.IntegerField()
    datetime = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_current_user)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('datetime', 'user',)

    def __str__(self):
        return self.user.username + " - " + str(self.datetime)