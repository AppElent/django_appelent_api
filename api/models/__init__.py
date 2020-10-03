import os
import importlib

__globals = globals()

from .Event import Event
from .Meterstand import Meterstand
from .OauthProvider import OauthProvider
from .OAuth2Token import OAuth2Token

# for file in os.listdir(os.path.dirname(__file__)):
#     mod_name = file[:-3]   # strip .py at the end
#     __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)