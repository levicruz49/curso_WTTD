from django.shortcuts import render
# Create your views here.
from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    context = {'form' : SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)