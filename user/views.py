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

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')


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
