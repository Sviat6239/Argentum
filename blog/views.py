from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import PostForm, CommentForm, HubForm
from .models import Post, Comment, Hub

@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    context = {}
    return render(request, template_name, context)

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
            return redirect('success')  
    return render(request, 'create_post.html', {'form': form})

@login_required
def update_post_view(request, f_id):
    post = get_object_or_404(Post, id=f_id)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'update_post.html', {'form': form, 'post': post})

@login_required
def delete_post_view(request, f_id):
    post = get_object_or_404(Post, id=f_id)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    if request.method == 'POST':
        post.delete()
        return redirect('success')
    return render(request, 'confirm_action.html', {'obj': post})

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
def update_comment_view(request, f_id):
    comment = get_object_or_404(Comment, id=f_id)
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
def delete_comment_view(request, f_id):
    comment = get_object_or_404(Comment, id=f_id)
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
            return redirect('success')
    return render(request, 'create_hub.html', {'form': form})

@login_required
def update_hub_view(request, f_id):
    hub = get_object_or_404(Hub, id=f_id)
    if hub.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this hub.")
    form = HubForm(instance=hub)
    if request.method == 'POST':
        form = HubForm(request.POST, instance=hub)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'update_hub.html', {'form': form, 'hub': hub})

@login_required
def delete_hub_view(request, f_id):
    hub = get_object_or_404(Hub, id=f_id)
    if hub.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this hub.")
    if request.method == 'POST':
        hub.delete()
        return redirect('success')
    return render(request, 'confirm_action.html', {'obj': hub})
