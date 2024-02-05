from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'


from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'your_app_name'
    verbose_name = 'Your App Name'