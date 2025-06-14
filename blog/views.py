from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from .forms import PostForm, CommentForm, HubForm
from .models import Post, Comment, Hub, Vote
from itertools import chain

def success_view(request):
    return render(request, 'success.html')

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    user_hubs = Hub.objects.filter(author=request.user)
    context = {
        'user_posts': user_posts,
        'user_hubs': user_hubs,
    }
    return render(request, 'dashboard.html', context)

# Post CRUD
@login_required
def create_post_view(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  
            return redirect('success')  
    return render(request, 'create_post.html', {'form': form})

@login_required
def update_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    if request.method == 'POST':
        post.delete()
        return redirect('success')
    return render(request, 'confirm_action.html', {'obj': post})

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'new_comment': new_comment
    }
    return render(request, 'post_detail.html', context)

# Comment CRUD
@login_required
def create_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('success')
    return render(request, 'create_comment.html', {'form': form, 'post': post})

@login_required
def update_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")
    form = CommentForm(instance=comment)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'update_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    if request.method == 'POST':
        comment.delete()
        return redirect('success')
    return render(request, 'confirm_action.html', {'obj': comment})

# Hub CRUD
@login_required
def create_hub_view(request):
    form = HubForm()
    if request.method == 'POST':
        form = HubForm(request.POST)
        if form.is_valid():
            hub = form.save(commit=False)
            hub.author = request.user
            hub.save()
            form.save_m2m()  
            return redirect('success')
    return render(request, 'create_hub.html', {'form': form})

@login_required
def update_hub_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    if hub.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this hub.")
    form = HubForm(instance=hub)
    if request.method == 'POST':
        form = HubForm(request.POST, instance=hub)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'edit_hub.html', {'form': form, 'hub': hub})

@login_required
def delete_hub_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    if hub.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this hub.")
    if request.method == 'POST':
        hub.delete()
        return redirect('success')
    return render(request, 'confirm_action.html', {'obj': hub})

@login_required
def hub_detail_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    posts = Post.objects.filter(hub=hub).order_by('-created_at')
    context = {
        'hub': hub,
        'posts': posts
    }
    return render(request, 'hub_detail.html', context)

# Voting Views
@login_required
def upvote_view(request, content_type, object_id):
    content_type_obj = get_object_or_404(ContentType, model=content_type)
    obj = get_object_or_404(content_type_obj.model_class(), id=object_id)
    vote, created = Vote.objects.get_or_create(
        user=request.user,
        content_type=content_type_obj,
        object_id=object_id,
        defaults={'value': 1}
    )
    if not created and vote.value != 1:
        vote.value = 1
        vote.save()
    return redirect(request.META.get('HTTP_REFERER', 'post_detail'))

@login_required
def downvote_view(request, content_type, object_id):
    content_type_obj = get_object_or_404(ContentType, model=content_type)
    obj = get_object_or_404(content_type_obj.model_class(), id=object_id)
    vote, created = Vote.objects.get_or_create(
        user=request.user,
        content_type=content_type_obj,
        object_id=object_id,
        defaults={'value': -1}
    )
    if not created and vote.value != -1:
        vote.value = -1
        vote.save()
    return redirect(request.META.get('HTTP_REFERER', 'post_detail'))

def recent_activity_view(request):
    last_hubs = Hub.objects.order_by('-created_at')[:5]
    
    posts = Post.objects.filter(hub__in=last_hubs).order_by('-created_at')[:20]
    
    context = {
        'posts': posts,
        'hubs': last_hubs,
    }
    return render(request, 'recent_activity.html', context)