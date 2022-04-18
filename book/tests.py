from django.test import TestCase

# Create your tests here.

from .models import Author, Book, PubHouse

class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Author.objects.create(firstname='Big', lastname='Bob')

    def test_first_name_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('firstname').verbose_name
        self.assertEquals(field_label,'имя')

    def test_last_name_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('lastname').verbose_name
        self.assertEquals(field_label,'фамилия')

    def test_description_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('description').verbose_name
        self.assertEquals(field_label,'Описание')

    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('firstname').max_length
        self.assertEquals(max_length,70)

    def test_last_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('lastname').max_length
        self.assertEquals(max_length,70)


    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = f'{author.firstname} {author.lastname}'
        self.assertEquals(expected_object_name,str(author))

    def test_get_url(self):
        author=Author.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_url(),'/author/big-bob/')



class PubHouseModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        PubHouse.objects.create(name_house='Cleaver')

    def test_name_house_label(self):
        pub_house=PubHouse.objects.get(id=1)
        field_label = pub_house._meta.get_field('name_house').verbose_name
        self.assertEquals(field_label,'название издательства')

    def test_email_label(self):
        pub_house=PubHouse.objects.get(id=1)
        field_label = pub_house._meta.get_field('email').verbose_name
        self.assertEquals(field_label,'почта')

    def test_address_label(self):
        pub_house=PubHouse.objects.get(id=1)
        field_label = pub_house._meta.get_field('address').verbose_name
        self.assertEquals(field_label,'адрес')

    def test_name_house_max_length(self):
        pub_house=PubHouse.objects.get(id=1)
        max_length = pub_house._meta.get_field('name_house').max_length
        self.assertEquals(max_length,70)

    def test_email_max_length(self):
        pub_house=PubHouse.objects.get(id=1)
        max_length = pub_house._meta.get_field('email').max_length
        self.assertEquals(max_length,70)

    def test_address_max_length(self):
        pub_house=PubHouse.objects.get(id=1)
        max_length = pub_house._meta.get_field('address').max_length
        self.assertEquals(max_length,200)

    def test_object_name_is_name_house(self):
        pub_house=PubHouse.objects.get(id=1)
        expected_object_name = pub_house.name_house
        self.assertEquals(expected_object_name,str(pub_house))

    def test_get_url(self):
        pub_house=PubHouse.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(pub_house.get_url(),'/pub_house/cleaver/')
