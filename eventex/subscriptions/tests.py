from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
# Create your tests here.

class SubscribeTest(TestCase):
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
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """ HTML MUST CONTAINS CSRF """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ CONTEXT MUST HAVE SUBSCRIPTION FORM """
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_fields(self):
        """ FORM MUST HAVE 4 FIELDS """
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(self.form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Levi Cruz', cpf='39612687785', email='leline22@gmail.com', phone='11-958523665')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """ VALID POST SHOULD REDIRECT TO /INSCRICAO/ """
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'levicruz49@gmail.com'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['levicruz49@gmail.com', 'leline22@gmail.com']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Levi Cruz', email.body)
        self.assertIn('39612687785', email.body)
        self.assertIn('leline22@gmail.com', email.body)
        self.assertIn('11-958523665', email.body)

class SubscribeInvalidPost(TestCase):

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

class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        self.data = dict(name='Levi Cruz', cpf='39612687785', email='leline22@gmail.com', phone='11-958523665')
        self.resp = self.client.post('/inscricao/', self.data, follow=True)

    def test_message(self):
        self.assertContains(self.resp, 'Inscrição realizada com sucesso!')