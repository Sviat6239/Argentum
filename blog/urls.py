from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


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
    path('discussion/create/', views.create_discussion_view, name='create_discussion'),
    path('discussion/<int:pk>/', views.discussion_detail_view, name='discussion_detail'),
    path('discussion/<int:pk>/edit/', views.edit_discussion_view, name='edit_discussion'),
    path('discussion/<int:pk>/delete/', views.delete_discussion_view, name='delete_discussion'),
    path('hub/<int:hub_id>/', views.hub_detail_view, name='hub_detail'),
    path('hub/<int:hub_id>/create_post/', views.create_post_view, name='create_post'),
    path('discussion/create/<int:hub_id>/', views.create_discussion_view, name='create_discussion'),
    path('hubs/', views.hubs_overview_view, name='hubs_overview'),
    path('hub/<int:hub_id>/follow/', views.follow_hub, name='follow_hub'),
    path('hub/<int:hub_id>/unfollow/', views.unfollow_hub, name='unfollow_hub'),
    path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('user/<int:user_id>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('user/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('user/<int:user_id>/posts/', views.user_posts, name='user_posts'),
    path('user/<int:user_id>/hubs/', views.user_hubs, name='user_hubs'),
    path('user/<int:user_id>/discussions/', views.user_discussions, name='user_discussions'),
    path('user/<int:user_id>/comments/', views.user_comments, name='user_comments'),
    path('user/<int:user_id>/followed_hubs/', views.user_followed_hubs, name='user_followed_hubs'),
    path('user/<int:user_id>/followers/', views.user_followers, name='user_followers'),
    path('user/<int:user_id>/following/', views.user_following, name='user_following'),
    path('following/', views.following_feed, name='following_feed'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)