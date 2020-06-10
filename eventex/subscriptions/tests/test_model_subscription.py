from datetime import datetime
from django.shortcuts import resolve_url as r
from django.test import TestCase
from eventex.subscriptions.models import *

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Levi Cruz',
            cpf='12345678901',
            email='levicruz49@gmail.com',
            phone='11-952589933'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_create_at(self):
        """ SUBSCRIPTION MUST HAVE AN AUTO CREATED_AT ATTR """
        self.assertIsInstance(self.obj.created_at, datetime)
    def test_str(self):
        self.assertEqual('Levi Cruz', str(self.obj))

    def test_paid_default_to_false(self):
        self.assertEqual(False, self.obj.paid)

    def test_get_absolut_url(self):
        url = r('subscriptions:detail', self.obj.hashid)
        self.assertEqual(url, self.obj.get_absolute_url())