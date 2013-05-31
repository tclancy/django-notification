from notification import backends
from templated_emails.utils import send_templated_email

from django.conf import settings
from django.contrib.sites.models import Site


class TemplatedEmailBackend(backends.BaseBackend):
    """
    At attempt to wire django-notifications to
    https://github.com/philippWassibauer/templated-emails
    not to
    https://github.com/bradwhittington/django-templated-email
    though that might be a good idea
    """
    spam_sensitivity = 0

    def deliver(self, recipient, sender, notice_type, extra_context):
        if recipient == sender:
            return False

        context = self.default_context()
        site = Site.objects.get_current()
        context.update({
            "recipient": recipient,
            "sender": sender,
            "site": site,
            "QUALIFIED_URL": "http://%s%s" % (site.domain, settings.STATIC_URL),
            'DOMAIN_URL': 'http://%s' % site.domain
        })
        context.update(extra_context)
        send_templated_email([recipient], "emails/%s" % notice_type, context)
        return True
