from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from .forms import CustomerForm, LoginUserForm, CustomerEditForm
from .models import Customer


menu = [{'title': "Добавить книгу", 'url_name': "add_book"},

        ]
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена</h1>')


class LoginUser(LoginView):
    """Представление входа"""
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
    """Представление выхода"""
    logout(request)
    return redirect('login')


class SignUp(CreateView):
    """Представление регистрации"""
    form_class = CustomerForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Представление редактирование профиля пользователя"""
    model = Customer
    template_name = 'registration/create_one.html'
    form_class = CustomerEditForm

    def get_success_url(self):
        return reverse('update_user', kwargs={'pk': self.kwargs['pk']})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """Представление удаление профиля пользователя"""
    model = Customer
    template_name = 'registration/delete_user.html'
    success_url = reverse_lazy('books')
