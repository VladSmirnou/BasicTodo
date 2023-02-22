from django.urls import path

from .views import (
    home_page,
    CreateUser, 
    LoginUser, 
    user_logout,
    CreatePost, 
    DeletePost, 
    UpdatePost,
    flash_message_cleaner,
)


urlpatterns = [
    path('', home_page, name='home_page'),
]

# Direct access via hardcoded URL path means that it is not htmx request
# and it breaks everything, don't know how to fix this.
# I tried to change headers to make a normal request object act like HTMX request object
# like this -> request.headers.__dict__['_store']['accept'] = ('Accept', '*/*')
# and like this -> request.META['HTTP_ACCEPT'] = '*/*' but Django doesn't save those changes at all.
# I tried to set headers in process_template_respose hook but it doesn't work either. Don't think that 
# process_request can help as well.
# One work-around that i found is to put method and action <form> attributes, so it will handle two types
# of requests, but it still redirects to a new URL and another htmx elements won't send any requests at all.

htmx_patterns = [
    path('create_user/', CreateUser.as_view(), name='create_user'),
    path('login_user/', LoginUser.as_view(), name='login_user'),
    path('logout_user/', user_logout, name='logout_user'),
    path('create_post/', CreatePost.as_view(), name='create_post'),
    path('delete_post/<int:pk>/', DeletePost.as_view(), name='delete_post'),
    path('update_post/<int:pk>/', UpdatePost.as_view(), name='update_post'),
    path('flash_message_cleaner/', flash_message_cleaner, name='flash_message_cleaner'),
]

urlpatterns += htmx_patterns