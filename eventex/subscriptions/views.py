from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.mixins import EmailCreateMixin
from eventex.subscriptions.models import Subscription


class EmailCreateView(EmailCreateMixin, CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_mail()
        return response


new = EmailCreateView.as_view(model=Subscription,
                              form_class=SubscriptionForm,
                              email_subject='Confirmação de inscrição')


class DescriptionDetailView(DetailView):
    def get_object(self, **kwargs):
        object = get_object_or_404(Subscription, hashid=self.kwargs['hashid'])
        return object
