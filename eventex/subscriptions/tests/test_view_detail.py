from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name='Levi Cruz',
            cpf='39612687785',
            email='leline22@gmail.com',
            phone='11-958523665'
        )
        self.resp = self.client.get(r('subscriptions:detail', self.obj.hashid))
        self.subscription = self.resp.context['subscription']

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_detail.html')

    def test_context(self):
        self.assertIsInstance(self.subscription, Subscription)

    def test_html(self):
        contents = (self.obj.name, self.obj.cpf, self.obj.email, self.obj.phone)
        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)


class subscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get(r('subscriptions:detail', '86a04bab-a8be-4d49-8c0e-11ae0c11daf9'))
        self.assertEqual(404, resp.status_code)