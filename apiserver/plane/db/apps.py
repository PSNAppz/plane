from django.apps import AppConfig


class DbConfig(AppConfig):
    name = "plane.db"

    def ready(self):
        # from . import signals # noqa
        # removed for now as there are inconsistencies on how roles are
        # handled
        pass