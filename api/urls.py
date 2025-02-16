from django.urls import path

from .views import user_auth
from .views import user_mgt
from .views import property
from .views import  booking

urlpatterns=[
    path('users/', user_mgt.get_users, name="get_users"),
    path('users/register/', user_mgt.register_user, name="register_user"),
    path('users/<int:pk>/', user_mgt.user_detail, name="user_detail"),
    path('users/login/', user_auth.user_login, name="login"),
    path('thread/', property.manage_thread, name="manage_thread"),
    path('thread/<int:pk>/', property.thread_detail, name="thread_detail"),
    path('thread/<int:fk>/post/', booking.manage_post, name="manage_post"),
    path('thread/<int:fk>/post/<int:pk>/', booking.post_detail, name="post_detail"),

]
