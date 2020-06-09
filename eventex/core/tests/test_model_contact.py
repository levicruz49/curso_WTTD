from django.core.exceptions import ValidationError
from django.test import TestCase

from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name= 'Levi Cruz',
            slug = 'levi-cruz',
            photo = 'http://hbn.link/hb-pic'
        )

    def test_email(self):
        contact = Contact.objects.create(speaker = self.speaker,kind=Contact.EMAIL,value='levicruz49@gmail.com')

        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(speaker = self.speaker,kind=Contact.PHONE,value='11-52932558')

        self.assertTrue(Contact.objects.exists())

    def test_choice(self):
        """ CONTACT KIND SHOULD BE LIMITED TO E OR P """
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL, value='levicruz49@gmail.com')
        self.assertEqual('levicruz49@gmail.com', str(contact))

class ContactManagersTest(TestCase):
    def setUp(self):
        self.s = Speaker.objects.create(
            name='Levi Cruz',
            slug='levi-cruz',
            photo='http://hbn.link/hb-pic'
        )

        self.s.contact_set.create(kind=Contact.EMAIL, value='levicruz49@gmail.com')
        self.s.contact_set.create(kind=Contact.PHONE, value='11-952908339')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['levicruz49@gmail.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phone(self):
        qs = Contact.objects.phones()
        expected = ['11-952908339']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)