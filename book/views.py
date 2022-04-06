from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import F, Avg, Count
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from .forms import CustomerForm, AddBookForm, CustomerUpdateForm
from .models import Author, PubHouse
from .models import Book, Customer


# Create your views here.
menu = [{'title': "Добавить книгу", 'url_name': "add_book"},
        {'title': "Войти", 'url_name': "login"},
        {'title': "Регистрация", 'url_name': "signup"}
]


def pageNotFound(request,exception):
    return HttpResponseNotFound('<h1> Страница не найдена</h1>')

def home(request):
    return render(request, "registration/home.html")


class SignUp(CreateView):
    form_class = CustomerForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"




class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'registration/create_one.html'
    fields = ['email', 'phone', 'age', 'sex']
    login_url='login'
    success_url = reverse_lazy('home')

    def get_object(self, *args, **kwargs):
        return self.request.user


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone[1:].isdigit():
            raise ValidationError('Поле должно быть формата +79876543211')
        if phone[0] != '+':
            raise ValidationError('Поле должно быть формата +79876543211')
        if len(phone) != 12:
            raise ValidationError('Поле должно быть формата +79876543211')
        return phone

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'registration/delete_user.html'
    success_url = reverse_lazy('books')

class AddBook(CreateView):
    form_class = AddBookForm
    template_name = 'book/add_book.html'
    success_url = reverse_lazy('books')



def all_authors(request):
    contact_list = Author.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    authors = Author.objects.order_by(F("lastname").asc(nulls_last=True))
    return render(request, 'author/all_authors.html', {
        'authors': authors,
        'menu': menu,
        'page_obj': page_obj

    })


def one_author(request, slug_author: str):
    author = get_object_or_404(Author, slug=slug_author)
    return render(request, 'author/one_author.html', {
        'author': author,

    })


def all_books(request):
    contact_list = Book.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    books = Book.objects.order_by(F("rating").asc(nulls_last=True))
    agg = books.aggregate(Avg('rating'), Count('id'))
    return render(request, 'book/all_books.html', {
        'books': books,
        'agg': agg,
        'menu': menu

    })


def one_books(request, slug_book: str):
    book = get_object_or_404(Book, slug=slug_book)
    return render(request, 'book/one_book.html', {
        'book': book,

    })


def all_pub_houses(request):
    pub_houses = PubHouse.objects.order_by(F("name_house").asc(nulls_last=True))
    agg_house = pub_houses.aggregate(Count('id'))
    return render(request, 'pub_house/all_pub_houses.html', {
        'pub_houses': pub_houses,
        'agg_house': agg_house,
        'menu': menu

    })


def one_pub_house(request, slug_pub_house: str):
    pub_house = get_object_or_404(PubHouse, slug=slug_pub_house)
    return render(request, 'pub_house/one_pub_house.html', {
        'pub_house': pub_house,

    })



# class CreateUser(CreateView):
#     model = Users
#     template_name = 'users/create.html'
#     fields = ['firstname', 'lastname', 'email', 'phone', 'age', 'sex']
#
# def users_create(request):
#     form = UsersForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('users')
#     else:
#         context = {'form': form}
#
#     return render(request, 'users/create.html', context)
#
#
# def one_create(request, id: int):
#     user = get_object_or_404(Users, id=id)
#     return render(request, 'users/create_one.html', {
#         'user': user
#     })

