from django.apps import AppConfig


class NotificationsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications_app'
    def ready(self):
        import notifications_app.signals