from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.core.models import Speaker

class SpeakerDetailGet(TestCase):

    def setUp(self):
        Speaker.objects.create(
            name='Grace Hopper',
            slug='grace-hopper',
            website='http://hbn.link/hopper-site',
            photo='http://hbn.link/hopper-pic',
            description='Programadora e almirante.',
        )
        self.resp = self.client.get(r('speaker_detail', slug='grace-hopper'))

    def test_get(self):
        """ GET SHOULD RETURN STATUS 200 """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/speaker_detail.html')

    def test_html(self):
        contains = [
            'Grace Hopper',
            'Programadora e almirante',
            'http://hbn.link/hopper-pic',
            'http://hbn.link/hopper-site',
        ]
        for expected in contains:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_context(self):
        """ SPEAKER MUST BE IN CONTEXT """
        speaker = self.resp.context['speaker']
        self.assertIsInstance(speaker, Speaker)

class SpeakerDetailNotFound(TestCase):
    def test_not_found(self):
        self.resp = self.client.get(r('speaker_detail', slug='not-found'))
        self.assertEqual(404, self.resp.status_code)