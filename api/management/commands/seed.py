from django.core.management.base import BaseCommand
import random, os
from datetime import datetime
from ...models import OauthProvider

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

""" Only create (doesnt clear data) """
MODE_CREATE = 'create'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print('Deleting oauthproviders')
    OauthProvider.objects.all().delete()

def get_base_url():
    env = os.getenv('ENVIRONMENT')
    if env == 'LOCAL':
        return 'http://localhost:8000'
    elif env == 'DEV':
        return 'https://appelent-api-dev.herokuapp.com'
    elif env == 'STAGING':
        return 'https://appelent-api-staging.herokuapp.com'
    elif env == 'PRODUCTION':
        return 'https://appelent-api.herokuapp.com'


def create_oauthproviders():
    """Creates an OauthProvider"""
    enelogic = OauthProvider(
        name='enelogic', 
        client_id='<replace this>', 
        client_secret='<replace this>', 
        access_token_url='https://enelogic.com/oauth/v2/token', 
        authorize_url='https://enelogic.com/oauth/v2/auth', 
        api_base_url='https://enelogic.com/api', 
        client_kwargs='{\'scope\': \'account\'}', 
        redirectUrl=(get_base_url() + '/api/oauth/enelogic/token'), 
        flow='authorization_code',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    enelogic.save()


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: create / refresh / clear 
    :return:
    """
    if mode is None:
        mode = MODE_CREATE
    # Clear data from tables
    if mode != MODE_CREATE:
        clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating OauthProviders
    create_oauthproviders()