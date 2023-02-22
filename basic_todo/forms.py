from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import UserPost


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            'username',
            'email',
            'password1',
            'password2',
        )


class CreatePostForm(ModelForm):
    class Meta:
        model = UserPost
        fields = [
            'post_title', 
            'post_context', 
        ]
