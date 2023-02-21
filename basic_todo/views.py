from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import CustomUserCreationForm, CreatePostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import UserPost
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest

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
        if request.htmx:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('home_page')

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
        if request.htmx:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('home_page')

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return redirect('home_page')

        return render(request, self.template_name, {'form': form})


class CreatePost(View): 
    form_class = CreatePostForm
    template_name = 'create_post.html'

    def get(self, request):
        # i can't use login_required decorator because redirect is a normal 
        # request
        if not request.user.is_authenticated:
            messages.error(request, 'You need to login first')
            return redirect('home_page')
        if request.htmx:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('home_page')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post_author_id = request.user.pk
            form.save()
            return redirect('home_page')
        
        return render(request, self.template_name, {'form': form})


class DeletePost(View):
    def delete(self, request, pk):
        # This check is for direct requests, like POST request from postman, etc., because 
        # this view doesn't support GET request, so it is impossible to get
        # this page.
        if request.user.is_authenticated and request.method == 'DELETE':
            try:
                post = UserPost.objects.get(post_author=request.user.pk, pk=pk)
                messages.success(request, f'Your post *{post.post_title}* was successfully deleted!')
                post.delete()
            except:
                messages.error(request, 'Post doesn\'t exist')
        else:
            messages.error(request, 'Forbidden')

        return redirect('home_page')


def user_logout(request):
    logout(request)
    return redirect('home_page')


def flash_message_cleaner(request):
    return HttpResponse('')
