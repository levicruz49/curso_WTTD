from django.test import TestCase

# Create your tests here.

class HomeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_get(self):
        """ GET / MUST RETURN STATUS CODE 200 """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ MUST USE INDEX.HTML """
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_subscription_lin(self):
        self.assertContains(self.resp, 'href="/inscricao/"')