from django.test import TestCase
from django.shortcuts import resolve_url as r

# Create your tests here.

class HomeTest(TestCase):
    fixtures = ['keynotes.json']


    def setUp(self):
        self.resp = self.client.get(r('home'))

    def test_get(self):
        """ GET / MUST RETURN STATUS CODE 200 """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ MUST USE INDEX.HTML """
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_subscription_lin(self):
        expected = 'href="{}"'.format(r('subscriptions:new'))
        self.assertContains(self.resp, expected)

    def test_speakers(self):
        """ MUST SHOW KEYNOTE SPEAKERS """
        contents = [
            'href="{}"'.format(r('speaker_detail', slug='grace-hopper')),
            'Grace Hopper',
            'http://hbn.link/hopper-pic',
            'href="{}"'.format(r('speaker_detail', slug='alan-turing')),
            'Alan Turing',
            'http://hbn.link/turing-pic',
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_speakers_link(self):
        expected = 'href="{}#speakers"'.format(r('home'))
        self.assertContains(self.resp, expected)