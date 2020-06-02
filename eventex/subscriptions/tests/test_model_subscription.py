from datetime import datetime

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