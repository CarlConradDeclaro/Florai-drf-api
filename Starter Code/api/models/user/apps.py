 # api/models/user/apps.py
from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.models.user'

    def ready(self):
        import api.models.user.signals
