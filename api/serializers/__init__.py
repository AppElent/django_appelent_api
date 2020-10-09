import os
import importlib

__globals = globals()

#from .serializers import *
from .EventSerializer import EventSerializer
from .MeterstandSerializer import MeterstandSerializer
from .OauthProviderSerializer import OauthProviderSerializer
from .OAuth2TokenSerializer import OAuth2TokenSerializer
from .Test1Serializer import Test1Serializer

# for file in os.listdir(os.path.dirname(__file__)):
#     mod_name = file[:-3]   # strip .py at the end
#     __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)