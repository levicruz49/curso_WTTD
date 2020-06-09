from django.test import TestCase

from eventex.core.managers import PeriodManager
from eventex.core.models import Talk, Course


class TalkModelTest(TestCase):
    def setUp(self):
        self.talk = Talk.objects.create(
            title = 'Titulo da Palestra',

        )

    def test_create(self):
        self.assertTrue(Talk.objects.exists())

    def test_has_speakers(self):
        """ TALK GAS MANY SPEAKERS AND VICE-VERSA """
        self.talk.speakers.create(
            name='Levi Cruz',
            slug='levi-cruz',
            website='http://levicruz.net'
        )
        self.assertEqual(1, self.talk.speakers.count())

    def test_description_blank(self):
        field = Talk._meta.get_field('description')
        self.assertTrue(field.blank)

    def test_speakers_blank(self):
        field = Talk._meta.get_field('speakers')
        self.assertTrue(field.blank)

    def test_start_blank(self):
        field = Talk._meta.get_field('start')
        self.assertTrue(field.blank)

    def test_start_null(self):
        field = Talk._meta.get_field('start')
        self.assertTrue(field.null)

    def test_str(self):
        self.assertEqual('Titulo da Palestra', str(self.talk))

class PeriodManagerTest(TestCase):
    def setUp(self):
        Talk.objects.create(title='Morning Talk', start='11:59')
        Talk.objects.create(title='Afternoon Talk', start='12:00')

    def test_manager(self):
        self.assertIsInstance(Talk.objects, PeriodManager)

    def test_at_morning(self):
        qs = Talk.objects.at_morning()
        expected = ['Morning Talk']
        self.assertQuerysetEqual(qs, expected, lambda o: o.title)

    def test_at_afternoon(self):
        qs = Talk.objects.at_afternoon()
        expected = ['Afternoon Talk']
        self.assertQuerysetEqual(qs, expected, lambda o: o.title)


class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='Titulo do curso',
            start='09:00',
            description='Descrição do curso',
            slots=20
        )

    def test_create(self):
        self.assertTrue(Course.objects.exists())

    def test_speaker(self):
        """ COURSE HAS MANY SPEAKERS AND VICE-VERSA """
        self.course.speakers.create(
            name='Levi Cruz',
            slug='levi-cruz',
            website='http://levicruz.net'
        )
        self.assertEqual(1, self.course.speakers.count())

    def test_str(self):
        self.assertEqual('Titulo do curso', str(self.course))

    def test_manager(self):
        self.assertIsInstance(Course.objects, PeriodManager)