from unittest.mock import Mock

from django.test import TestCase
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin

class SubscriptionModelAdminTest(TestCase):
    def setUp(self):
        Subscription.objects.create(name='Levi Cruz', cpf='39612687785',
                                    email='levicruz49@gmail.com', phone='11-958523665')
        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)

    def test_has_action(self):
        """ ACTION MARK_AS_PAID SHOUD BE INSTALLED """
        self.assertIn('mark_as_paid', self.model_admin.actions)

    def test_mark_all(self):
        """ IT SHOULD MARK ALL SELECTED SUBSCRIPTIONS AS PAID """
        self.call_action()
        self.assertEqual(1, Subscription.objects.filter(paid=True).count())

    def test_message(self):
        """ IT SHOULD SEND A MESSAGE TO THE USER """
        mock = self.call_action()
        mock.assert_called_once_with(None, '1 inscrição foi marcada como paga.')

    def call_action(self):
        queryset = Subscription.objects.all()

        mock = Mock()
        old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = mock

        self.model_admin.mark_as_paid(None, queryset)

        SubscriptionModelAdmin.message_user = old_message_user

        return mock