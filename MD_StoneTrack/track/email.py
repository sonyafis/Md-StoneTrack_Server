from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from djoser import email

class PasswordResetEmail(email.PasswordResetEmail):
    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context.update({
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
            "domain": get_current_site(self.request).domain,
            "protocol": "https" if self.request.is_secure() else "http",
        })
        print(f"Generated reset link: {context['protocol']}://{context['domain']}/auth/password/reset/confirm/{context['uid']}/{context['token']}/")
        return context