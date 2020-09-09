from django.apps import AppConfig


class CovidUsersConfig(AppConfig):
    name = 'covidUsers'
    verbose_name = "Dashboard"

    def ready(self):
        import covidUsers.signals
