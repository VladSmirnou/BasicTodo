from django_htmx.http import retarget

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib import messages

from .models import UserPost
from .forms import CustomUserCreationForm, CreatePostForm
from .utils import login_request_check

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
    # i don't want to allow a user that's
    # already authenticated to crete a new user
    @login_request_check(not_=True)
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @login_request_check(not_=True)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_user')

        return render(request, self.template_name, {'form': form})


class LoginUser(View):
    form_class = AuthenticationForm
    template_name = 'auth/login_user.html'

    @login_request_check(not_=True)
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return redirect('home_page')

        return render(request, self.template_name, {'form': form})


class CreatePost(View): 
    form_class = CreatePostForm
    template_name = 'create_post.html'

    @login_request_check()
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @login_request_check()
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            post_title = form.cleaned_data.get('post_title')
            form = form.save(commit=False)
            form.post_author_id = request.user.pk
            form.save()
            messages.success(request, f'Your post *{post_title}* was successfully created!')
            return redirect('home_page')
        
        return render(request, self.template_name, {'form': form})


class DeletePost(View):
    def delete(self, request, pk):
        if request.user.is_authenticated and request.htmx and request.method == 'DELETE':
            try:
                post = UserPost.objects.get(post_author=request.user.pk, pk=pk)
                messages.success(request, f'Your post *{post.post_title}* was successfully deleted!')
                post.delete()
            except:
                messages.error(request, 'Post doesn\'t exist')
        else:
            messages.error(request, 'Forbidden')

        return redirect('home_page')


class UpdatePost(View):
    form_class = CreatePostForm
    template_name = 'update_post.html'

    @login_request_check()
    def get(self, request, pk):
        try:
            post = UserPost.objects.get(post_author=request.user.pk, pk=pk)
            form = self.form_class(instance=post)
            return render(request, self.template_name, {'form': form})
        except:
            messages.error(request, 'Post doesn\'t exist')
            return redirect('home_page')

    @login_request_check()
    def post(self, request, pk):
        try:
            old_post = UserPost.objects.get(post_author=request.user.pk, pk=pk)
        except:
            messages.error(request, 'Post doesn\'t exist')
            return redirect('home_page')

        form = self.form_class(request.POST, instance=old_post)
        if form.is_valid():
            form.save()
            return redirect('home_page')
        
        error_form = self.form_class(instance=old_post)
        error_form.cleaned_data = form.cleaned_data
        for field in form.errors:
            error_form.add_error(field, form.errors[field])
        response = render(request, self.template_name, {'form': error_form})
        return retarget(response, '#error')


def user_logout(request):
    logout(request)
    return redirect('home_page')


def flash_message_cleaner(request):
    return HttpResponse('')
