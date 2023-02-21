from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import UserPost
from django.http import HttpResponse
from django.contrib import messages

# Even tho gunicorn pre-forks processes i still can add multiple threads 
# per one process, so it's better to use class-based view, cus at least Django 
# terminates an instance after a view is done and instances don't share
# their dictionaries data

def home_page(request):
    user_posts = UserPost.objects.all()
    return render(request, 'home.html', {'user_posts': user_posts})


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


class DeletePost(View):
    def delete(self, request, pk):
        try:
            post = UserPost.objects.get(post_author=request.user.pk, pk=pk)
            messages.success(request, f'Your post *{post.post_title}* was successfully deleted!')
            post.delete()
        except:
            messages.error(request, 'Forbidden')
        return redirect('home_page')


def user_logout(request):
    logout(request)
    return redirect('home_page')


def flash_message_cleaner(request):
    return HttpResponse('')