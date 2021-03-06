from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class EmailCreateMixin:
    email_to = None
    email_context_name = None
    email_template_name = None
    email_from = settings.DEFAULT_FROM_EMAIL
    email_subject = ''

    def send_mail(self):
        # Send email
        subject = self.email_subject
        from_ = self.email_from
        to = self.get_email_to()
        template_name = self.get_email_template_name()
        context = self.get_email_context_data()

        body = render_to_string(template_name, context)
        send_mail(subject, body, from_, [from_, to])

    def get_email_template_name(self):
        if self.email_template_name:
            return self.email_template_name

        meta = self.object._meta
        return '{}/{}_email.txt'.format(meta.app_label, meta.model_name)

    def get_email_context_data(self, **kwargs):
        context = dict(kwargs)
        context.setdefault(self.get_email_context_name(), self.object)
        return context

    def get_email_context_name(self):
        if self.email_context_name:
            return self.email_context_name
        return self.object._meta.model_name

    def get_email_to(self):
        if self.email_to:
            return self.email_to
        return self.object.email


class SubscriptionCreate(EmailCreateMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    email_subject = 'Confirmação de inscrição'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_mail()

        return response