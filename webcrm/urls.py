from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from common.views.favicon import FaviconRedirect
from crm.views.contact_form import contact_form
from crm.views.public_request import public_request
from massmail.views.get_oauth2_tokens import get_refresh_token
from kyc.api import upload_kyc_endpoint
from crm.views.kyc_views import auto_create_contact_view

urlpatterns = [
    path('favicon.ico', FaviconRedirect.as_view()),
    path('voip/', include('voip.urls')),
    path('hijack/', include('hijack.urls')),
    # Tenant-aware public request endpoint: /en/<agency_id>/request/
    path('<int:agency_id>/request/', public_request, name='public_request'),
    path(
        'OAuth-2/authorize/',
        staff_member_required(get_refresh_token), 
        name='get_refresh_token'
    ),
    path('api/kyc/upload/', upload_kyc_endpoint, name='kyc_upload'),
    path('api/crm/contact/auto-create/', auto_create_contact_view, name='auto_create_contact'),
    path('api/urbaty/', include('urbaty.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]

urlpatterns += i18n_patterns(
    path(settings.SECRET_CRM_PREFIX, include('common.urls')),
    path(settings.SECRET_CRM_PREFIX, include('crm.urls')),
    path(settings.SECRET_CRM_PREFIX, include('massmail.urls')),
    path(settings.SECRET_CRM_PREFIX, include('tasks.urls')),
    path(settings.SECRET_ADMIN_PREFIX, admin.site.urls),
    path('contact-form/<uuid:uuid>/', contact_form, name='contact_form'),
)
