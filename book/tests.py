# Create your tests here.

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.test import TestCase, Client

from user.models import Customer
from .models import Author, PubHouse, Book

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
        Book.objects.create(title='test1', rating='90', creator=creator)

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'название')

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_description_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_rating_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('rating').verbose_name
        self.assertEquals(field_label, 'Рейтинг')

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEquals(max_length, 70)

    def test_object_name_is_book(self):
        book = Book.objects.get(id=1)
        expected_object_name = f'{book.title} - {book.rating}'
        self.assertEquals(expected_object_name, str(book))

    def test_book_has_slug(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.slug, slugify(book.title))

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.get_absolute_url(), '/book/test1/')


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
        assert response.status_code == 302, f'Status code is not 302! code={response.status_code}'
        book = Book.objects.get(id=1)
        assert book
        assert book.creator == self.test_user, 'Book creator is not test_user!'
        assert book.author == Author.objects.get(id=1)
        assert book.pub_house.first() == self.pub_house, f'Book pub_house={book.pub_house}, pub_house must be {self.pub_house}'

    def edit_book(self):
        self.client.force_login(self.test_user)
        book = Book.objects.create(title='test-book')
        # response = self.client.post(reverse('add_book'), data={
        #     'title': 'Test book',
        #     'description': 'Some text',
        #     'author': '1',
        #     'pub_house': [str(self.pub_house.id)]
        # })
        # assert response.status_code == 302, f'Status code is not 302! code={response.status_code}'
        # book = Book.objects.get(id=1)
        # assert book
        # assert book.creator == self.test_user, 'Book creator is not test_user!'
        # assert book.author == Author.objects.get(id=1)
        # assert book.pub_house.first() == self.pub_house, f'Book pub_house={book.pub_house}, pub_house must be {self.pub_house}'
        response = self.client.get(reverse('/book/test-book/'))
        assert response.status_code == 200, 'Код ответа не 200!'
        client_post_response = self.client.post(
            reverse('/book/test-book/update/',
            {
            'title': 'Updated title',
            'description': 'Updated text',
        }
                    ))
        self.assertEqual(client_post_response.status_code, 302)
        book.refresh_from_db()
        assert book.title == 'Updated title', f'Заголовок не поменялся! Текущее значение: {book.title}'
        assert book.description == 'Updated text' ,f'Описание не поменялось! Текущее значение: {book.description}'



    def delete_book(self):
        self.client.force_login(self.test_user)
        book = Book.objects.create(title='test-book')
        # response = self.client.post(reverse('add_book'), data={
        #     'title': 'Test book',
        #     'description': 'Some text',
        #     'author': '1',
        #     'pub_house': [str(self.pub_house.id)]
        # })
        # assert response.status_code == 302, f'Status code is not 302! code={response.status_code}'
        # book = Book.objects.get(id=1)
        # assert book
        # assert book.creator == self.test_user, 'Book creator is not test_user!'
        # assert book.author == Author.objects.get(id=1)
        # assert book.pub_house.first() == self.pub_house, f'Book pub_house={book.pub_house}, pub_house must be {self.pub_house}'
        response = self.client.get(reverse('/book/test-book/'))
        assert response.status_code == 200, 'Код ответа не 200!'
        client_delete_response = self.client.post(
            reverse('/book/test-book/delete/'))
        self.assertEqual(client_delete_response.status_code, 302)


class TestAuthorAll(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.test_user = User.objects.create(username='test_user')

    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13
        for author_num in range(number_of_authors):
            Author.objects.create(firstname='Christian %s' % author_num, lastname='Surname %s' % author_num, )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/author/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('author'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('author'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'author/all_authors.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('author'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        # self.assertTrue( len(resp.context['all_authors']) == 5)

    def test_context_data(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('author'))
        assert response.context['menu'], 'Context data has no menu object!'


class TestPubHouseAll(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.test_user = User.objects.create(username='test_user')

    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_pub_house = 13
        for pub_house_num in range(number_of_pub_house):
            PubHouse.objects.create(name_house='test %s' % pub_house_num, email='test %s' % pub_house_num, )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/pub_house/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('pub_house'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('pub_house'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'pub_house/all_pub_houses.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('pub_house'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        # self.assertTrue( len(resp.context['all_pub_houses']) == 5)

    def test_context_data(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('pub_house'))
        assert response.context['menu'], 'Context data has no menu object!'


class TestBookAll(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.test_user = User.objects.create(username='test_user')

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(firstname='first', lastname='last')
        cls.pub_house = PubHouse.objects.create(name_house='Test house', email='example@mail.com')

    def test_book_creator(self):
        self.client.force_login(self.test_user)
        Book.objects.create(title='test1', description='test', creator=self.test_user)
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/all_books.html')

    def test_context_data(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse('books'))
        assert response.context['menu'], 'Context data has no menu object!'



class TestShowAuthor(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.test_user = User.objects.create(username='test_user')

    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        test_author = Author.objects.create(firstname='author', lastname='test')

    def test_login_required(self):
        author = Author.objects.get(id=1)
        response = self.client.get('/author/author-test/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test')
        self.assertTemplateUsed(response, 'author/one_author.html')

    def test_context_data(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/author/author-test/')
        assert response.context['menu'], 'Context data has no menu object!'


class TestShowPubHouse(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.test_user = User.objects.create(username='test_user')

    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        test_pub_house = PubHouse.objects.create(name_house='test', email='test')

    def test_login_required(self):
        pub_house = PubHouse.objects.get(id=1)
        response = self.client.get('/pub_house/test/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test')
        self.assertTemplateUsed(response, 'pub_house/one_pub_house.html')

    def test_context_data(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/pub_house/test/')
        assert response.context['menu'], 'Context data has no menu object!'

# class TestShowBook(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.client = Client()
#         cls.test_user = User.objects.create(username='test_user')
#
#     def test_post_detailtest_post_detail(self):
#         book = Book.objects.create(title='test1', creator=self.test_user, description='test')
#         response = self.client.get(reverse('/book/test1/'))
#         assert response.status_code == 200, 'Код ответа не 200!'
        # assert response.context['post'] == post, 'Неверный объект в контексте!'

# class TestSearchBook(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.client = Client()
#         cls.test_user = User.objects.create(username='test_user')
#
#     @classmethod
#     def setUpTestData(cls):
#         Author.objects.create(firstname='first', lastname='last')
#         cls.pub_house = PubHouse.objects.create(name_house='Test house', email='example@mail.com')
#
#     def test_book_creator(self):
#         self.client.force_login(self.test_user)
#         Book.objects.create(title='test1', description='test', creator=self.test_user)
#         response = self.client.get('/search_book/')


class CustomerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Customer.objects.create(username='Big', email='lshdj@mail.ru', password='qwerty')

    def test_phone_label(self):
        user = Customer.objects.get(id=1)
        field_label = user._meta.get_field('phone').verbose_name
        self.assertEquals(field_label, 'телефон')

    def test_age_label(self):
        user = Customer.objects.get(id=1)
        field_label = user._meta.get_field('age').verbose_name
        self.assertEquals(field_label, 'возраст')

    def test_sex_label(self):
        user = Customer.objects.get(id=1)
        field_label = user._meta.get_field('sex').verbose_name
        self.assertEquals(field_label, 'пол')

    def test_sex_max_length(self):
        user = Customer.objects.get(id=1)
        max_length = user._meta.get_field('sex').max_length
        self.assertEquals(max_length, 10)


class TestAddCustomerView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.test_user = User.objects.create(username='test_user')


    # @classmethod
    # def setUpTestData(cls):
    #     # Set up non-modified objects used by all test methods
    #     Customer.objects.create(username='Big', password='qwerty')

    def test_login_required(self):
        unauthorized_client = Client()
        response = unauthorized_client.get(reverse('/signup/'))
        assert response.status_code == 302, 'Unauthorized user does not redirected to login page!'




    # def test_context_data(self):
    #     self.client.force_login(self.test_user)
    #     response = self.client.get(reverse('add_book'))
    #     assert response.context['menu'], 'Context data has no menu object!'
    #     assert response.context['form'], 'Context data has no form!'
    #
    # def test_book_creator(self):
    #     self.client.force_login(self.test_user)
    #     response = self.client.post(reverse('add_book'), data={
    #         'title': 'Test book',
    #         'description': 'Some text',
    #         'author': '1',
    #         'pub_house': [str(self.pub_house.id)]
    #     })
    #     assert response.status_code == 302, f'Status code is not 302! code={response.status_code}'
    #     book = Book.objects.get(id=1)
    #     assert book
    #     assert book.creator == self.test_user, 'Book creator is not test_user!'
    #     assert book.author == Author.objects.get(id=1)
    #     assert book.pub_house.first() == self.pub_house, f'Book pub_house={book.pub_house}, pub_house must be {self.pub_house}'
