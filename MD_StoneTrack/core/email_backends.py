from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
import random


class MultiSMTPEmailBackend:
    def __init__(self, *args, **kwargs):
        self.backends = [
            EmailBackend(
                host=config['HOST'],
                port=config['PORT'],
                username=config['USER'],
                password=config['PASSWORD'],
                use_tls=config.get('USE_TLS', False),
                use_ssl=config.get('USE_SSL', False),
                fail_silently=kwargs.get('fail_silently', False)
            ) for config in settings.EMAIL_BACKENDS
        ]

    def send_messages(self, email_messages):
        backend = random.choice(self.backends)
        return backend.send_messages(email_messages)