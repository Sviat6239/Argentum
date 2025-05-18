from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from .forms import PostForm, CommentForm, HubForm, DiscussionForm
from .models import Post, Comment, Hub, Vote, Discussion
from Argentum.models import UserProfile
from Argentum.forms import UserProfileForm

def success_view(request):
    return render(request, 'success.html')

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    user_hubs = Hub.objects.filter(author=request.user)
    
    post_count = user_posts.count()
    hub_count = user_hubs.count()
    
    post_content_type = ContentType.objects.get_for_model(Post)
    comment_content_type = ContentType.objects.get_for_model(Comment)
    
    upvotes = Vote.objects.filter(
        user=request.user,
        value=1,
        content_type__in=[post_content_type, comment_content_type],
        object_id__in=list(user_posts.values_list('id', flat=True)) + list(Comment.objects.filter(author=request.user).values_list('id', flat=True))
    ).count()
    
    downvotes = Vote.objects.filter(
        user=request.user,
        value=-1,
        content_type__in=[post_content_type, comment_content_type],
        object_id__in=list(user_posts.values_list('id', flat=True)) + list(Comment.objects.filter(author=request.user).values_list('id', flat=True))
    ).count()

    context = {
        'user_posts': user_posts,
        'user_hubs': user_hubs,
        'post_count': post_count,
        'hub_count': hub_count,
        'upvotes': upvotes,
        'downvotes': downvotes,
    }
    return render(request, 'dashboard.html', context)

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


def hub_detail_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    posts = Post.objects.filter(hub=hub).order_by('-created_at')
    context = {
        'hub': hub,
        'posts': posts
    }
    return render(request, 'hub_detail.html', context)

# Discussion CRUD

@login_required
def create_discussion_view(request, hub_id):
    hub = get_object_or_404(Hub, pk=hub_id)
    if request.method == 'POST':
        form = DiscussionForm(request.POST, user=request.user)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.hub = hub
            discussion.save()
            form.save_m2m()
            return redirect('discussion_detail', discussion_id=discussion.id)
    else:
        form = DiscussionForm(user=request.user, initial={'hub': hub})
    return render(request, 'create_discussion.html', {'form': form, 'hub': hub})

@login_required
def update_discussion_view(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id, author=request.user)
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion, user=request.user)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.save()
            form.save_m2m()
            return redirect('discussion_detail', discussion_id=discussion.id)
    else:
        form = DiscussionForm(instance=discussion, user=request.user)
    return render(request, 'update_discussion.html', {'form': form, 'discussion': discussion})

@login_required
def delete_discussion_view(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id, author=request.user)
    if request.method == 'POST':
        discussion.delete()
        return redirect('dashboard')
    return render(request, 'delete_discussion.html', {'discussion': discussion})

def discussion_detail_view(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    comments = discussion.comments.all()
    comment_form = CommentForm() if request.user.is_authenticated else None
    return render(request, 'discussion_detail.html', {
        'discussion': discussion,
        'comments': comments,
        'is_author': request.user.is_authenticated and request.user == discussion.author,
        'comment_form': comment_form,
    })
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


@login_required
def edit_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user, name=request.user.username)
        profile.save()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'bio': request.user.bio,
            'profile_picture': request.user.profile_picture,
        }
        form = UserProfileForm(instance=profile, user=request.user, initial=initial)

    user_posts = Post.objects.filter(author=request.user)
    user_hubs = Hub.objects.filter(author=request.user)
    user_discussions = Discussion.objects.filter(author=request.user)

    return render(request, 'dashboard.html', {
        'form': form,
        'post_count': user_posts.count(),
        'hub_count': user_hubs.count(),
        'discussion_count': user_discussions.count(),
        'upvotes': sum(post.vote_count for post in user_posts) if user_posts else 0,
        'downvotes': sum(1 for vote in Vote.objects.filter(content_type=ContentType.objects.get_for_model(Post), object_id__in=user_posts.values('id'), value=-1)) if user_posts else 0,
        'user_posts': user_posts,
        'user_hubs': user_hubs,
        'user_discussions': user_discussions,
    })