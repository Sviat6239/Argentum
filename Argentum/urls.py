"""
URL configuration for Argentum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import (
    dashboard, create_post_view, show_post_view, update_post_view, delete_post_view,
    create_comment_view, show_comment_view, update_comment_view, delete_comment_view,
    create_hub_view, show_hub_view, update_hub_view, delete_hub_view

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='index'),  # Homepage redirects to dashboard
    path('dashboard/', dashboard, name='dashboard'),
    # Post URLs
    path('posts/create/', create_post_view, name='create_post'),
    path('posts/', show_post_view, name='view_post'),
    path('posts/update/<int:f_id>/', update_post_view, name='update_post'),
    path('posts/delete/<int:f_id>/', delete_post_view, name='delete_post'),
    # Comment URLs
    path('comments/create/<int:post_id>/', create_comment_view, name='create_comment'),
    path('comments/<int:post_id>/', show_comment_view, name='view_comment'),
    path('comments/update/<int:f_id>/', update_comment_view, name='update_comment'),
    path('comments/delete/<int:f_id>/', delete_comment_view, name='delete_comment'),
    # Hub URLs
    path('hubs/create/', create_hub_view, name='create_hub'),
    path('hubs/', show_hub_view, name='view_hub'),
    path('hubs/update/<int:f_id>/', update_hub_view, name='update_hub'),
    path('hubs/delete/<int:f_id>/', delete_hub_view, name='delete_hub'),
]
