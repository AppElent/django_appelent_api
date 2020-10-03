import os
import importlib

__globals = globals()

#from .views import *
from .EventViewSet import EventViewSet
from .MeterstandViewSet import MeterstandViewSet
from .OauthProviderViewSet import OauthProviderViewSet
from .Tado import *
from .OAuth2TokenViewSet import OAuth2TokenViewSet
from .Enelogic import *
from .SolarEdge import *
from .Oauth import *
from .tests import *

# for file in os.listdir(os.path.dirname(__file__)):
#     mod_name = file[:-3]   # strip .py at the end
#     __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)