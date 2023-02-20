from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

# Even tho gunicorn pre-forks processes i still can add multiple threads 
# per one process, so it's better to use class-based view, cus at least Django 
# terminates an instance after a view is done and instances don't share
# their dictionaries data

def home_page(request):
    return render(request, 'home.html')


class CreateUser(View):
    form_class = CustomUserCreationForm
    template_name = 'auth/create_user.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_user')

        return render(request, self.template_name, {'form': form})


class LoginUser(View):
    form_class = AuthenticationForm
    template_name = 'auth/login_user.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return redirect('home_page')

        return render(request, self.template_name, {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home_page')
