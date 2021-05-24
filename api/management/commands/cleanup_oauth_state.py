from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.utils import timezone
from ...models import Oauth2State


class Command(BaseCommand):
    help = "Deleting expires OAuth2State"

    # def add_arguments(self, parser):
    #     parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        Oauth2State.objects.filter(created_at__lte=timezone.now()-timedelta(minutes=10)).delete()
