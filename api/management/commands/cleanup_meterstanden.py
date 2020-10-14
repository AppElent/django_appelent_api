from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from ...models import Meterstand


class Command(BaseCommand):
    help = "Deleting Meterstanden from more than 7 days old."

    # def add_arguments(self, parser):
    #     parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        Meterstand.objects.filter(datetime=datetime.now()-timedelta(days=7)).delete()
