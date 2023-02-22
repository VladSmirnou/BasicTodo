from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=100, 
        blank=False, 
        help_text='This field is requeired',
    )


class UserPost(models.Model):
    post_author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=55)
    post_context = models.TextField(max_length=55)
    post_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post_title}'