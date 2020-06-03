from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Levi Cruz', cpf='39612687785', email='leline22@gmail.com', phone='11-958523665')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'levicruz49@gmail.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['levicruz49@gmail.com', 'leline22@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Levi Cruz',
            '39612687785',
            'leline22@gmail.com',
            '11-958523665',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)