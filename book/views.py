from django.shortcuts import render, get_object_or_404
from .models import Book
from django.db.models import F, Sum, Avg, Max, Min, Count
# Create your views here.
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
