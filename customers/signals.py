from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django_tenants.utils import schema_context
from django_tenants.signals import post_schema_sync # <-- The Magic Import
from .models import Domain

# We changed this from post_save to post_schema_sync
@receiver(post_schema_sync)
def auto_provision_tenant(sender, tenant, **kwargs):
    """
    Automatically creates the routing Domain and a default Admin user 
    AFTER the schema is fully built and migrated by django-tenants.
    """
    # Only run this for brand new agencies (ignore the public schema)
    if tenant.schema_name != 'public':
        
        # 1. AUTO-CREATE THE DOMAIN
        # This maps 'agency2' to 'agency2.localhost'
        base_domain = "localhost" 
        tenant_domain = f"{tenant.schema_name}.{base_domain}"
        
        Domain.objects.get_or_create(
            domain=tenant_domain,
            tenant=tenant,
            is_primary=True
        )

        # 2. AUTO-CREATE THE ADMIN USER
        with schema_context(tenant.schema_name):
            User = get_user_model()
            
            default_username = f"admin_{tenant.schema_name}"
            default_email = f"admin@{tenant_domain}"
            default_password = "ChangeMe123!"

            if not User.objects.filter(username=default_username).exists():
                User.objects.create_superuser(
                    username=default_username, 
                    email=default_email, 
                    password=default_password
                )