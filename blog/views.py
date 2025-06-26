from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from .forms import PostForm, CommentForm, HubForm, CategoryForm, TagForm, DiscussionForm
from .models import Post, Comment, Hub, Vote, Category, Tag, Discussion
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
        'user_discussions': Discussion.objects.filter(author=request.user),
    }
    return render(request, 'dashboard.html', context)

# Post CRUD
@login_required
def create_post_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.hub = hub
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('hub_detail', hub_id=hub.id)
    else:
        form = PostForm(initial={'hub': hub})
    return render(request, 'create_post.html', {'form': form, 'hub': hub})

@login_required
def update_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = PostForm(instance=post)
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

def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent')
            parent = Comment.objects.get(id=parent_id) if parent_id else None
            Comment.objects.create(
                post=post,
                content=form.cleaned_data['content'],
                author=request.user,
                parent=parent
            )
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    comments = post.comments.filter(parent__isnull=True).prefetch_related('replies', 'author')
    return render(
        request,
        'post_detail.html',
        {
            'post': post,
            'form': form,
            'comments': comments,
        }
    )

# Comment CRUD
@login_required
def create_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('success')
    else:
        form = CommentForm()
    return render(request, 'create_comment.html', {'form': form, 'post': post})

@login_required
def update_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = CommentForm(instance=comment)
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
    if request.method == 'POST':
        form = HubForm(request.POST)
        if form.is_valid():
            hub = form.save(commit=False)
            hub.author = request.user
            hub.save()
            form.save_m2m()
            return redirect('success')
    else:
        form = HubForm()
    return render(request, 'create_hub.html', {'form': form})

@login_required
def update_hub_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    if hub.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this hub.")
    if request.method == 'POST':
        form = HubForm(request.POST, instance=hub)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HubForm(instance=hub)
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

def hub_detail_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    posts = Post.objects.filter(hub=hub).prefetch_related('tags', 'author')
    discussions = Discussion.objects.filter(hub=hub).prefetch_related('tag', 'author')
    if request.method == 'POST':
        if 'post_submit' in request.POST:
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.hub = hub
                post.author = request.user
                post.save()
                post_form.save_m2m()
                return redirect('hub_detail', hub_id=hub.id)
        elif 'discussion_submit' in request.POST:
            discussion_form = DiscussionForm(request.POST)
            if form.is_valid():
                discussion = discussion_form.save(commit=False)
                discussion.hub = hub
                discussion.author = request.user
                discussion.save()
                discussion_form.save_m2m()
                return redirect('hub_detail', hub_id=hub.id)
    else:
        post_form = PostForm(initial={'hub': hub})
        discussion_form = DiscussionForm(initial={'hub': hub})
    context = {
        'hub': hub,
        'posts': posts,
        'discussions': discussions,
        'post_form': post_form,
        'discussion_form': discussion_form,
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
    return redirect(request.META.get('HTTP_REFERER', 'success'))

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
    return redirect(request.META.get('HTTP_REFERER', 'success'))

def get_post_votes(post):
    upvotes = post.votes.filter(value=1).count()
    downvotes = post.votes.filter(value=-1).count()
    return upvotes, downvotes

def get_hub_total_votes(hub):
    from django.db.models import Sum
    agg = hub.posts.aggregate(total=Sum('votes__value'))
    return agg['total'] or 0

def recent_activity_view(request):
    last_hubs = Hub.objects.order_by('-created_at')[:5]
    posts = Post.objects.filter(hub__in=last_hubs).order_by('-created_at')[:20]
    context = {
        'posts': posts,
        'hubs': last_hubs,
        'discussions': Discussion.objects.filter(hub__in=last_hubs).order_by('-created_at')[:5],
    }
    return render(request, 'recent_activity.html', context)

@login_required
def create_discussion_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.hub = hub
            discussion.author = request.user
            discussion.save()
            form.save_m2m()
            return redirect('hub_detail', hub_id=hub.id)
    else:
        form = DiscussionForm(initial={'hub': hub})
    return render(request, 'create_discussion.html', {'form': form, 'hub': hub})

@login_required
def edit_discussion_view(request, pk):
    discussion = get_object_or_404(Discussion, id=pk)
    if request.user != discussion.author:
        return HttpResponseForbidden("You are not allowed to edit this discussion.")
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            return redirect('discussion_detail', pk=discussion.id)
    else:
        form = DiscussionForm(instance=discussion)
    return render(request, 'edit_discussion.html', {'form': form, 'discussion': discussion})

@login_required
def delete_discussion_view(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if discussion.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this discussion.")
    if request.method == 'POST':
        discussion.delete()
        return redirect('success')
    return render(request, 'confirm_action.html', {'obj': discussion})

def discussion_detail_view(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    comments = Comment.objects.filter(discussion=discussion, parent__isnull=True).prefetch_related('replies', 'author')
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.discussion = discussion
            parent_id = request.POST.get('parent')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            return redirect('discussion_detail', pk=discussion.pk)
    else:
        form = CommentForm()
    return render(request, 'discussion_detail.html', {
        'discussion': discussion,
        'comments': comments,
        'form': form
    })