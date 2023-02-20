from django.urls import path
from .views import (
    home_page,
    CreateUser, 
    LoginUser, 
    user_logout, 
    DeletePost, 
    flash_message_cleaner
)


urlpatterns = [
    path('', home_page, name='home_page'),
]

htmx_patterns = [
    path('create_user/', CreateUser.as_view(), name='create_user'),
    path('login_user/', LoginUser.as_view(), name='login_user'),
    path('logout_user/', user_logout, name='logout_user'),
    path('delete_post/<int:pk>/', DeletePost.as_view(), name='delete_post'),
    path('flash_message_cleaner', flash_message_cleaner, name='flash_message_cleaner'),
]

urlpatterns += htmx_patterns