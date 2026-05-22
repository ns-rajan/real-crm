import sys
from tendo.singleton import SingleInstanceException
from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class CommonConfig(AppConfig):
    name = 'common'
    verbose_name = _('Common')
    label = 'common'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        # Implicitly connect a signal handler
        from common.signals.handlers import user_creation_handler   # NOQA
        
        # Prevent background tasks from running during database builds and terminal commands
        is_management_command = len(sys.argv) > 1 and sys.argv[1] in [
            'makemigrations', 'migrate', 'migrate_schemas', 'shell'
        ]
        
        if is_management_command:
            return  # Stop here, do not boot up the email or reminder threads

        from common.utils.notif_email_sender import NotifEmailSender

        self.nes = NotifEmailSender()       # NOQA
        self.nes.start()
        
        if not settings.TESTING:
            from common.utils.reminders_sender import RemindersSender
            try:
                self.rs = RemindersSender()     # NOQA
                self.rs.start()
            except SingleInstanceException:
                pass