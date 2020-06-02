from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
# Create your tests here.
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')
        self.form = self.resp.context['form']

    def test_get(self):
        """ GET /inscricao/ MUST RETURN STATUS COD 200 """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ MUST USE SUBSCRIPIONS/SUBSCRIPTION_FORM.HTML """
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """ HTML MUST CONTAIN INPUT TAGS """
        tags = (
                ('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"',1),

            )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """ HTML MUST CONTAINS CSRF """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ CONTEXT MUST HAVE SUBSCRIPTION FORM """
        self.assertIsInstance(self.form, SubscriptionForm)



class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Levi Cruz', cpf='39612687785', email='levicruz49@gmail.com', phone='11-958523665')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """ VALID POST SHOULD REDIRECT TO /INSCRICAO/ """
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())

class SubscribePostInvalid(TestCase):

    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})
        self.form = self.resp.context['form']
    def test_post(self):
        """ INVALID POST SHOULD NOT REDIRECT """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_error(self):
        self.assertTrue(self.form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())

class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        self.data = dict(name='Levi Cruz', cpf='39612687785', email='levicruz49@gmail.com', phone='11-958523665')
        self.resp = self.client.post('/inscricao/', self.data, follow=True)

    def test_message(self):
        self.assertContains(self.resp, 'Inscrição realizada com sucesso!')
