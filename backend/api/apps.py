from django.apps import AppConfig
import os

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        from .utils import start_scheduler
        if os.environ.get("RUN_MAIN") == "true":
            start_scheduler()
