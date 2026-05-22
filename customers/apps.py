from django.apps import AppConfig


class CustomersConfig(AppConfig):
    name = 'customers'
    
    def ready(self):
        # Wake up the auto-provisioning signal when the app starts
        import customers.signals