from tastypie.models import create_api_key
from django.contrib.auth.models import User
from django.db import models

models.signals.post_save.connect(create_api_key, sender=User)