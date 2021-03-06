from django.test import TestCase
from django.shortcuts import resolve_url as r

from eventex.core.models import Talk, Speaker, Course


class TalkListGet(TestCase):
    def setUp(self):
        t1 = Talk.objects.create(title='Titulo da Palestra', start='10:00', description='Descrição da palestra')
        t2 = Talk.objects.create(title='Titulo da Palestra', start='13:00', description='Descrição da palestra')
        c1 = Course.objects.create(title='Titulo do curso', start='09:00', description='Descrição do curso', slots=20)

        speaker = Speaker.objects.create(
            name='Levi Cruz',
            slug='levi-cruz',
            website='http://levicruz.net'
        )

        t1.speakers.add(speaker)
        t2.speakers.add(speaker)
        c1.speakers.add(speaker)


        self.resp = self.client.get(r('talk_list'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/talk_list.html')

    def test_html(self):
        contents = [
            (2, 'Titulo da Palestra'),
            (1, '10:00'),
            (1, '13:00'),
            (3, '/palestrantes/levi-cruz/'),
            (3, 'Levi Cruz'),
            (2, 'Descrição da palestra'),
            (1, 'Titulo do curso'),
            (1, '09:00'),
            (1, 'Descrição do curso')

        ]
        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected, count)


    def test_context(self):
        variables = ['talk_list']

        for key in variables:
            with self.subTest():
                self.assertIn(key, self.resp.context)


class TalkListGetEmpty(TestCase):
    def test_get_empty(self):
        response = self.client.get(r('talk_list'))

        self.assertContains(response, 'Ainda não existe palestras de manhã')
        self.assertContains(response, 'Ainda não existe palestras de tarde')