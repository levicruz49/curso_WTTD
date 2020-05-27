from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
# Create your tests here.

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/incricao/')
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