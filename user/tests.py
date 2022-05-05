# Create your tests here.

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.test import TestCase, Client

from .models import Customer

User = get_user_model()


class CustomerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Customer.objects.create(username='Big', password1='qwerty', password2='qwerty')

    # def test_first_name_label(self):
    #     author = Author.objects.get(id=1)
    #     field_label = author._meta.get_field('firstname').verbose_name
    #     self.assertEquals(field_label, 'имя')
    #
    # def test_last_name_label(self):
    #     author = Author.objects.get(id=1)
    #     field_label = author._meta.get_field('lastname').verbose_name
    #     self.assertEquals(field_label, 'фамилия')
    #
    # def test_description_label(self):
    #     author = Author.objects.get(id=1)
    #     field_label = author._meta.get_field('description').verbose_name
    #     self.assertEquals(field_label, 'Описание')
    #
    # def test_first_name_max_length(self):
    #     author = Author.objects.get(id=1)
    #     max_length = author._meta.get_field('firstname').max_length
    #     self.assertEquals(max_length, 70)
    #
    # def test_last_name_max_length(self):
    #     author = Author.objects.get(id=1)
    #     max_length = author._meta.get_field('lastname').max_length
    #     self.assertEquals(max_length, 70)
    #
    # def test_object_name_is_last_name_comma_first_name(self):
    #     author = Author.objects.get(id=1)
    #     expected_object_name = f'{author.firstname} {author.lastname}'
    #     self.assertEquals(expected_object_name, str(author))
    #
    # def test_author_has_slug(self):
    #     author = Author.objects.get(id=1)
    #     self.assertEqual(author.slug, slugify(f'{author.firstname} {author.lastname}'))
    #
    # def test_get_url(self):
    #     author = Author.objects.get(id=1)
    #     self.assertEquals(author.get_url(), '/author/big-bob/')
