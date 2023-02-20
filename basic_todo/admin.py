from django.contrib import admin
from .models import CustomUser, UserPost


admin.site.register([CustomUser, UserPost])
