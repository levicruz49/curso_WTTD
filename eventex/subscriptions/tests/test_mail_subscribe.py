from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Levi Cruz', cpf='39612687785', email='levicruz49@gmail.com', phone='11-958523665')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com', 'levicruz49@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Levi Cruz',
            '39612687785',
            'levicruz49@gmail.com',
            '11-958523665',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)