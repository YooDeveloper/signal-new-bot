import random 
import pendulum
import validators

from .models import *
from .connect import db

from tgbot.config import load_config
config = load_config(".env")
