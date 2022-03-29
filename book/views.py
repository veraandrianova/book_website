from django.db.models import F, Avg, Count
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import DetailView, UpdateView
from .models import Author, PubHouse
from .models import Book, Users
from .forms import UsersForm
from django.views.generic.edit import CreateView

# Create your views here.
def all_authors(request):
    authors = Author.objects.order_by(F("lastname").asc(nulls_last=True))
    return render(request, 'author/all_authors.html', {
        'authors': authors,

    })


def one_author(request, slug_author: str):
    author = get_object_or_404(Author, slug=slug_author)
    return render(request, 'author/one_author.html', {
        'author': author,

    })


def all_books(request):
    books = Book.objects.order_by(F("rating").asc(nulls_last=True))
    agg = books.aggregate(Avg('rating'), Count('id'))
    return render(request, 'book/all_books.html', {
        'books': books,
        'agg': agg

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

    })


def one_pub_house(request, slug_pub_house: str):
    pub_house = get_object_or_404(PubHouse, slug=slug_pub_house)
    return render(request, 'pub_house/one_pub_house.html', {
        'pub_house': pub_house,

    })

# class BlogDetailView(DetailView):
#     model = Users
#     template_name = 'create.html'
#
#
# class BlogCreateView(CreateView): # новое изменение
#     model = Users
#     template_name = 'create_one.html'
#     fields = ['firstname', 'lastname', 'email', 'phone', 'sex', 'age']

def users_create(request):
    error = ''
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book')
        else:
            error = 'Заполните все поля'
    form = UsersForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'users/create.html', data)


def one_create(request, id: int):
    user = get_object_or_404(Users,id = id)
    return render(request, 'users/create_one.html', {
        'user': user
     })
class NewsUpdateNew(UpdateView):
    model = Users
    template_name = 'create.html'
    fields = ['firstname', 'lastname', 'email', 'phone', 'sex', 'age']



