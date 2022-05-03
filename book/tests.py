# Create your tests here.

from django.test import TestCase, Client
from django.template.defaultfilters import slugify
from .models import Author, PubHouse, Book
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

User = get_user_model()
# Create your tests here.


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(firstname='Big', lastname='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('firstname').verbose_name
        self.assertEquals(field_label, 'имя')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('lastname').verbose_name
        self.assertEquals(field_label, 'фамилия')

    def test_description_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('firstname').max_length
        self.assertEquals(max_length, 70)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('lastname').max_length
        self.assertEquals(max_length, 70)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.firstname} {author.lastname}'
        self.assertEquals(expected_object_name, str(author))

    def test_author_has_slug(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.slug, slugify(f'{author.firstname} {author.lastname}'))

    def test_get_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        print(author.slug)
        self.assertEquals(author.get_url(), '/author/big-bob/')


class PubHouseModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        PubHouse.objects.create(name_house='Cleaver')

    def test_name_house_label(self):
        pub_house = PubHouse.objects.get(id=1)
        field_label = pub_house._meta.get_field('name_house').verbose_name
        self.assertEquals(field_label, 'название издательства')

    def test_email_label(self):
        pub_house = PubHouse.objects.get(id=1)
        field_label = pub_house._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'почта')

    def test_address_label(self):
        pub_house = PubHouse.objects.get(id=1)
        field_label = pub_house._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'адрес')

    def test_name_house_max_length(self):
        pub_house = PubHouse.objects.get(id=1)
        max_length = pub_house._meta.get_field('name_house').max_length
        self.assertEquals(max_length, 70)

    def test_email_max_length(self):
        pub_house = PubHouse.objects.get(id=1)
        max_length = pub_house._meta.get_field('email').max_length
        self.assertEquals(max_length, 70)

    def test_address_max_length(self):
        pub_house = PubHouse.objects.get(id=1)
        max_length = pub_house._meta.get_field('address').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_is_name_house(self):
        pub_house = PubHouse.objects.get(id=1)
        expected_object_name = pub_house.name_house
        self.assertEquals(expected_object_name, str(pub_house))

    def test_pub_house_has_slug(self):
        pub_house = PubHouse.objects.get(id=1)
        self.assertEqual(pub_house.slug, slugify(pub_house.name_house))

    def test_get_url(self):
        pub_house = PubHouse.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(pub_house.get_url(), '/pub_house/cleaver/')



class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        creator = User.objects.create(username='test_user')
        Book.objects.create(title='test1', creator=creator)

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'название')


class TestAddBookView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.test_user = User.objects.create(username='test_user')

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(firstname='first', lastname='last')
        cls.pub_house = PubHouse.objects.create(name_house='Test house', email='example@mail.com')


    def test_login_required(self):
        unauthorized_client = Client()
        response = unauthorized_client.get(reverse('add_book'))
        assert response.status_code == 302, 'Unauthorized user does not redirected to login page!'

    def test_authorized_user_get(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('add_book'))
        assert response.status_code == 200, f'Status code is not 200! code={response.status_code}'

    def test_context_data(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('add_book'))
        assert response.context['menu'], 'Context data has no menu object!'
        assert response.context['form'], 'Context data has no form!'

    def test_book_creator(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('add_book'), data={
            'title': 'Test book',
            'description': 'Some text',
            'author': '1',
            'pub_house': [str(self.pub_house.id)]
        })
        assert response.status_code == 302,  f'Status code is not 302! code={response.status_code}'
        book = Book.objects.get(id=1)
        assert book
        assert book.creator == self.test_user, 'Book creator is not test_user!'
        assert book.author == Author.objects.get(id=1)
        assert book.pub_house.first() == self.pub_house, f'Book pub_house={book.pub_house}, pub_house must be {self.pub_house}'

