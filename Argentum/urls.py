from django.contrib import admin
from django.urls import path, include
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

    # Success page
    path('success/', index, name='success'),

    # Blog app URLs (includes posts, comments, hubs, and voting)
    path('', include('blog.urls')),
]