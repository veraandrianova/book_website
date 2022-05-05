from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin

from .forms import AddBookForm, BookEditForm, RewiewForm, SearchForm
from .models import Author, PubHouse, Book

# Create your views here.
menu = [{'title': "Добавить книгу", 'url_name': "add_book"},

        ]

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена</h1>')


class AddBook(LoginRequiredMixin, CreateView):
    form_class = AddBookForm
    template_name = 'book/add_book.html'

    def form_valid(self, form):
        print(self.request.POST)
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

    def get_context_data(self, *args, object_list=None, **kwargs):
        kwargs['update'] = True
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].creator:
            return self.handle_no_permission()
        return kwargs


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'book/delete_book.html'
    success_url = reverse_lazy('books')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def delete(self, request, *args, **kwargs):
        self.book = self.get_object()
        success_url = self.get_success_url()
        if self.request.user != self.object.creator:
            return self.handle_no_permission()
        self.object.delete()
        return HttpResponseRedirect(success_url)


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
    queryset = Book.objects.filter(is_published=True)

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


class ShowBook(FormMixin, DetailView):
    model = Book
    template_name = 'book/one_book.html'
    form_class = RewiewForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['books_selected'] = 0
        print(context)
        return context

    def get_success_url(self):
        slug = self.kwargs['slug']

        return reverse('book_details', kwargs={'slug': slug})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        form = self.get_form()
        return self.form_valid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.book = self.get_object()
        self.object.creator = self.request.user
        self.object.save()
        # return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.book = self.get_object()
    #     # self.success_url = self.get_success_url()
    #     self.object.creator = self.request.user
    #
    #     self.object.save()
    #     return redirect(self.success_url)


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

class SearchBook(ListView):
    model = Book
    template_name = 'book/all_books.html'
    context_object_name = "books"
    form_class = SearchForm

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['menu'] = menu
    #     return context
    #
    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     books = Book.objects.filter(
    #         Q(title__icontains=query)
    #
    #     )
    #     return books
    def get_queryset(self):
        print(self.request.GET.get('q'))
        queryset = Book.objects.filter(title__icontains=self.request.GET.get("q").title())
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q")
        context['menu'] = menu
        return context



class SearchAuthor(ListView):
    model = Author
    template_name = 'author/all_authors.html'
    context_object_name = "authors"

    def get_queryset(self):
        print(self.request.GET.get('q'))
        queryset = Author.objects.filter(lastname__icontains=self.request.GET.get("q").title())
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q")
        context['menu'] = menu
        return context

class SearchPubHouse(ListView):
    model = PubHouse
    template_name = 'pub_house/all_pub_houses.html'
    context_object_name = "pub_houses"

    def get_queryset(self):
        print(self.request.GET.get('q'))
        queryset = PubHouse.objects.filter(name_house__icontains=self.request.GET.get("q").title())
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q")
        context['menu'] = menu
        return context
