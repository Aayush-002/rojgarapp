from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
    verbose_name = _("Rojgar App")
