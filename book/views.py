from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.db.models import Q
from .forms import AddBookForm, BookEditForm, RewiewForm
from .models import Author, PubHouse, Book


menu = [{'title': "Добавить книгу", 'url_name': "add_book"},
        {'title': "Поиск", 'url_name': "search"},

        ]


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена</h1>')


class BookAll(ListView):
    """Представление просмотра всех книг"""
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


class ShowBook(FormMixin, DetailView):
    """Представление просмотра книги детально"""
    model = Book
    template_name = 'book/one_book.html'
    form_class = RewiewForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['books_selected'] = 0
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
        return super().form_valid(form)


class AddBook(LoginRequiredMixin, CreateView):
    """Представление добавления книги"""
    form_class = AddBookForm
    template_name = 'book/add_book.html'

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
    """Представление редактирования книги"""
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
    """Представление удаления книги"""
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
    """Представление просмотра всех авторов"""
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


class ShowAuthor(DetailView):
    """Представление просмотра автора детально"""
    model = Author
    template_name = 'author/one_author.html'
    context_object_name = "author"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['authors_selected'] = 0
        return context


class PubHouseAll(ListView):
    """Представление просмотра всех издательств"""
    paginate_by = 3
    model = PubHouse
    template_name = "pub_house/all_pub_houses.html"
    context_object_name = "pub_houses"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['pub_houses_selected'] = 0
        print(context)

        return context


class ShowPubHouse(DetailView):
    """Представление просмотра издательства детально"""
    model = PubHouse
    template_name = 'pub_house/one_pub_house.html'
    context_object_name = "pub_house"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['pub_houses_selected'] = 0
        return context


class SearchView(TemplateView):
    """Представление поиска книги, автора, издательства"""
    template_name = 'search/search_results.html'

    def get_authors(self):
        authors = Author.objects.none()
        if self.request.GET.get('q'):
            authors = Author.objects.filter(Q(lastname__icontains=self.request.GET.get('q').title()) |
                                            Q(firstname__icontains=self.request.GET.get('q').title()))
        return authors

    def get_books(self):
        books = Book.objects.none()
        if self.request.GET.get('q'):
            books = Book.objects.filter(title__icontains=self.request.GET.get('q').title())
        return books

    def get_pub_houses(self):
        pub_houses = PubHouse.objects.none()
        if self.request.GET.get('q'):
            pub_houses = PubHouse.objects.filter(name_house__icontains=self.request.GET.get('q').title())
        return pub_houses

    def get_object_list(self):
        object_list = []
        for book in self.get_books():
            object_dict = {
                'type': 'book',
                'title': book.title,
                'url': book.get_absolute_url(),
                'object': book
            }
            object_list.append(object_dict)

        for author in self.get_authors():
            object_dict = {
                'type': 'author',
                'lastname': author.lastname,
                'firstname': author.firstname,
                'object': author
            }
            object_list.append(object_dict)

        for pub_house in self.get_pub_houses():
            object_dict = {
                'type': 'pub_house',
                'name_house': pub_house.name_house,
                'object': pub_house
            }
            object_list.append(object_dict)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_object_list()
        return context
