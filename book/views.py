from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import CustomerForm, AddBookForm, LoginUserForm, CustomerEditForm, BookEditForm
from .models import Author, PubHouse
from .models import Book, Customer

# Create your views here.
menu = [{'title': "Добавить книгу", 'url_name': "add_book"},

        ]


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена</h1>')


def home(request):
    return render(request, "registration/home.html")


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "registration/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('update_user', kwargs={'pk': user_id})


def logout_user(request):
    logout(request)
    return redirect('login')


class SignUp(CreateView):
    form_class = CustomerForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'registration/create_one.html'
    form_class = CustomerEditForm
    login_url = 'login'
    success_url = reverse_lazy('books')

    # def get_object(self, *args, **kwargs):
    #     return self.request.user


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'registration/delete_user.html'
    success_url = reverse_lazy('books')



class AddBook(LoginRequiredMixin, CreateView):
    form_class = AddBookForm
    template_name = 'book/add_book.html'


    def get_object(self, *args, **kwargs):
         return self.request.user


    def form_valid(self, form):
        book = form.save(commit=False)
        book.creator = self.request.user
        book.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class BookEditView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'book/book_edit.html'
    form_class = BookEditForm
    success_url = reverse_lazy('books')
    slug_url_kwarg = 'slug_book'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


    def form_valid(self, form):
        book = form.save(commit=False)
        book.creator = self.request.book
        book.save()
        return super().form_valid(form)



class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'book/delete_book.html'
    success_url = reverse_lazy('books')
    slug_url_kwarg = 'slug_book'

class AuthorAll(ListView):
    paginate_by = 3
    model = Author
    template_name = "author/all_authors.html"
    context_object_name = "authors"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['author_selected'] = 0
        return context


# def all_authors(request):
#     contact_list = Author.objects.all()
#     paginator = Paginator(contact_list, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     authors = Author.objects.order_by(F("lastname").asc(nulls_last=True))
#     return render(request, 'author/all_authors.html', {
#         'authors': authors,
#         'menu': menu,
#         'page_obj': page_obj
#
#     })
class ShowAuthor(DetailView):
    model = Author
    template_name = 'author/one_author.html'
    context_object_name = "author"
    slug_url_kwarg = 'slug_author'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['authors_selected'] = 0
        return context


# def one_author(request, slug_author: str):
#     author = get_object_or_404(Author, slug=slug_author)
#     return render(request, 'author/one_author.html', {
#         'author': author,
#
#     })

class BookAll(ListView):
    paginate_by = 3
    model = Book
    template_name = "book/all_books.html"
    context_object_name = "books"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['books_selected'] = 0
        return context


# def all_books(request):
#     contact_list = Book.objects.all()
#     paginator = Paginator(contact_list, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     books = Book.objects.order_by(F("rating").asc(nulls_last=True))
#     agg = books.aggregate(Avg('rating'), Count('id'))
#     return render(request, 'book/all_books.html', {
#         'books': books,
#         'agg': agg,
#         'menu': menu,
#         'page_obj': page_obj
#
#     })


class ShowBook(DetailView):
    model = Book
    template_name = 'book/one_book.html'
    context_object_name = "book"
    slug_url_kwarg = 'slug_book'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['books_selected'] = 0
        return context


# def one_books(request, slug_book: str):
#     book = get_object_or_404(Book, slug=slug_book)
#     return render(request, 'book/one_book.html', {
#         'book': book,
#
#     })


class PubHouseAll(ListView):
    paginate_by = 3
    model = PubHouse
    template_name = "pub_house/all_pub_houses.html"
    context_object_name = "pub_houses"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['pub_houses_selected'] = 0
        return context


# def all_pub_houses(request):
#     pub_houses = PubHouse.objects.order_by(F("name_house").asc(nulls_last=True))
#     agg_house = pub_houses.aggregate(Count('id'))
#     return render(request, 'pub_house/all_pub_houses.html', {
#         'pub_houses': pub_houses,
#         'agg_house': agg_house,
#         'menu': menu
#
#     })


class ShowPubHouse(DetailView):
    model = PubHouse
    template_name = 'pub_house/one_pub_house.html'
    context_object_name = "pub_house"
    slug_url_kwarg = 'slug_pub_house'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['pub_houses_selected'] = 0
        return context

# def one_pub_house(request, slug_pub_house: str):
#     pub_house = get_object_or_404(PubHouse, slug=slug_pub_house)
#     return render(request, 'pub_house/one_pub_house.html', {
#         'pub_house': pub_house,
#
#     })


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
