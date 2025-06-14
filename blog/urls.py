from django.urls import path
from . import views

urlpatterns = [
    path('success/', views.success_view, name='success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post/create/', views.create_post_view, name='create_post'),
    path('post/<int:post_id>/edit/', views.update_post_view, name='update_post'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('comment/<int:post_id>/create/', views.create_comment_view, name='create_comment'),
    path('comment/<int:comment_id>/edit/', views.update_comment_view, name='update_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'),
    path('hub/create/', views.create_hub_view, name='create_hub'),
    path('hub/<int:hub_id>/edit/', views.update_hub_view, name='update_hub'),
    path('hub/<int:hub_id>/delete/', views.delete_hub_view, name='delete_hub'),
    path('hub/<int:hub_id>/', views.hub_detail_view, name='hub_detail'),
    path('vote/<str:content_type>/<int:object_id>/upvote/', views.upvote_view, name='upvote'),
    path('vote/<str:content_type>/<int:object_id>/downvote/', views.downvote_view, name='downvote'),
    path('recent/', views.recent_activity_view, name='recent_activity'),
]