from django.contrib import admin
from django.urls import path
from autentification.views import login_view, logout_view, register_view
from blog.views import (
    dashboard,
    create_post_view, post_detail_view, update_post_view, delete_post_view,
    create_comment_view, update_comment_view, delete_comment_view,
    create_hub_view, hub_detail_view, update_hub_view, delete_hub_view
)
from Argentum.views import index

urlpatterns = [
    # Authentication
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    # Admin panel
    path('admin/', admin.site.urls),

    # Home page
    path('', index, name='index'),

    # User dashboard
    path('dashboard/', dashboard, name='dashboard'),

    path('success/', index, name='success'),

    # Posts
    path('posts/create/', create_post_view, name='create_post'),
    path('posts/<int:post_id>/', post_detail_view, name='post_detail'),
    path('posts/update/<int:post_id>/', update_post_view, name='update_post'),
    path('posts/delete/<int:post_id>/', delete_post_view, name='delete_post'),

    # Comments
    path('comments/create/<int:post_id>/', create_comment_view, name='create_comment'),
    path('comments/update/<int:comment_id>/', update_comment_view, name='update_comment'),
    path('comments/delete/<int:comment_id>/', delete_comment_view, name='delete_comment'),

    # Hubs
    path('hubs/create/', create_hub_view, name='create_hub'),
    path('hubs/<int:hub_id>/', hub_detail_view, name='hub_detail'),
    path('hubs/update/<int:hub_id>/', update_hub_view, name='update_hub'),
    path('hubs/delete/<int:hub_id>/', delete_hub_view, name='delete_hub'),
]
