from django.shortcuts import render, get_object_or_404
from .models import Book
from .models import Author, PubHouse
from django.db.models import F, Sum, Avg, Max, Min, Count
# Create your views here.
def all_authors(request):
    authors = Author.objects.order_by(F("lastname").asc(nulls_last=True))
    return render(request, 'author/all_authors.html', {
        'authors': authors,

    })

def one_author(request, slug_author:str):
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

def one_books(request, slug_book:str):
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

def one_pub_house(request, slug_pub_house:str):
    pub_house = get_object_or_404(PubHouse, slug=slug_pub_house)
    return render(request, 'pub_house/one_pub_house.html', {
        'pub_house': pub_house,

    })
