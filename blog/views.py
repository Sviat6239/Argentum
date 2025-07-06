from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from .forms import PublicChatForm, PrivateChatForm, MessageForm, PostForm, CommentForm, HubForm, DiscussionForm
from .models import PublicChat, PrivateChat, Message, PublicChatRole, Attachment, Post, Comment, Hub, Vote, Category, Tag, Discussion, FollowingHub, FollowingUser
from django.contrib.auth import get_user_model
import os

User = get_user_model()

def get_comment_level(comment):
    level = 0
    current = comment
    while current.parent:
        level += 1
        current = current.parent
    return level

def success_view(request):
    return render(request, "success.html")

@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user)
    user_hubs = Hub.objects.filter(author=request.user)
    followed_hubs = request.user.followed_hubs.all()  
    context = {
        "user_posts": user_posts,
        "user_hubs": user_hubs,
        "user_discussions": Discussion.objects.filter(author=request.user),
        "followed_hubs": followed_hubs,
    }
    return render(request, "dashboard.html", context)

# Post CRUD
@login_required
def create_post_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.hub = hub
            post.author = request.user
            post.save()
            form.save_m2m()

            files = request.FILES.getlist("attachments")
            for file in files:
                Attachment.objects.create(
                    content_object=post,
                    file=file,
                    uploaded_by=request.user,
                )
            return redirect("hub_detail", hub_id=hub.id)
    else:
        form = PostForm(initial={"hub": hub})
    return render(request, "create_post.html", {"form": form, "hub": hub})


@login_required
def update_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            files = request.FILES.getlist("attachments")
            for file in files:
                Attachment.objects.create(
                    content_object=post,
                    file=file,
                    uploaded_by=request.user,
                )
            return redirect("success")
    else:
        form = PostForm(instance=post)
    return render(request, "edit_post.html", {"form": form, "post": post})


@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    if request.method == "POST":
        hub_id = post.hub.id
        post.delete()
        return redirect("hub_detail", hub_id=hub_id)
    return render(request, "confirm_action.html", {"obj": post})


def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post, parent__isnull=True).prefetch_related(
        "replies", "author", "attachments"
    )
    post.attachments_with_basename = [
        {"file": attachment.file, "basename": os.path.basename(attachment.file.name)}
        for attachment in post.attachments.all()
    ]
    for comment in comments:
        comment.attachments_with_basename = [
            {"file": attachment.file, "basename": os.path.basename(attachment.file.name)}
            for attachment in comment.attachments.all()
        ]
        comment.indentation = get_comment_level(comment) * 20

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            parent_id = request.POST.get("parent")
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            files = request.FILES.getlist("attachments")
            for file in files:
                Attachment.objects.create(
                    content_object=comment,
                    file=file,
                    uploaded_by=request.user,
                )
            return redirect("post_detail", post_id=post.id)
    else:
        form = CommentForm()

    return render(
        request,
        "post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
        },
    )


# Comment CRUD
@login_required
def create_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get("parent")
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            files = request.FILES.getlist("attachments")
            for file in files:
                Attachment.objects.create(
                    content_object=comment,
                    file=file,
                    uploaded_by=request.user,
                )
            return redirect("post_detail", post_id=post.id)
    else:
        form = CommentForm()
    return render(request, "create_comment.html", {"form": form, "post": post})


@login_required
def update_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this comment.")
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save()
            files = request.FILES.getlist("attachments")
            for file in files:
                Attachment.objects.create(
                    content_object=comment,
                    file=file,
                    uploaded_by=request.user,
                )
            return redirect(
                "discussion_detail" if comment.discussion else "post_detail",
                pk=comment.discussion.id if comment.discussion else comment.post.id,
            )
    else:
        form = CommentForm(instance=comment)
    return render(request, "update_comment.html", {"form": form, "comment": comment})


@login_required
def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    if request.method == "POST":
        redirect_view = "discussion_detail" if comment.discussion else "post_detail"
        redirect_id = (
            comment.discussion.id if comment.discussion else comment.post.id
        )
        comment.delete()
        return redirect(redirect_view, pk=redirect_id)
    return render(request, "confirm_action.html", {"obj": comment})


# Hub CRUD
@login_required
def create_hub_view(request):
    if request.method == "POST":
        form = HubForm(request.POST)
        if form.is_valid():
            hub = form.save(commit=False)
            hub.author = request.user
            hub.save()
            form.save_m2m()
            return redirect("success")
    else:
        form = HubForm()
    return render(request, "create_hub.html", {"form": form})


@login_required
def update_hub_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    if hub.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this hub.")
    if request.method == "POST":
        form = HubForm(request.POST, instance=hub)
        if form.is_valid():
            form.save()
            return redirect("success")
    else:
        form = HubForm(instance=hub)
    return render(request, "edit_hub.html", {"form": form, "hub": hub})


@login_required
def delete_hub_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    if hub.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this hub.")
    if request.method == "POST":
        hub.delete()
        return redirect("success")
    return render(request, "confirm_action.html", {"obj": hub})


def hub_detail_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    posts = Post.objects.filter(hub=hub).prefetch_related("tags", "author")
    discussions = Discussion.objects.filter(hub=hub).prefetch_related("tags", "author")
    followed_hubs = (
        request.user.followed_hubs.all()
        if request.user.is_authenticated
        else []
    )

    if request.method == "POST":
        if "post_submit" in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            discussion_form = DiscussionForm(initial={"hub": hub})
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.hub = hub
                post.author = request.user
                post.save()
                post_form.save_m2m()
                files = request.FILES.getlist("attachments")
                for file in files:
                    Attachment.objects.create(
                        content_object=post,
                        file=file,
                        uploaded_by=request.user,
                    )
                return redirect("hub_detail", hub_id=hub.id)

        elif "discussion_submit" in request.POST:
            discussion_form = DiscussionForm(request.POST, request.FILES)
            post_form = PostForm(initial={"hub": hub})
            if discussion_form.is_valid():
                discussion = discussion_form.save(commit=False)
                discussion.hub = hub
                discussion.author = request.user
                discussion.save()
                discussion_form.save_m2m()
                files = request.FILES.getlist("attachments")
                for file in files:
                    Attachment.objects.create(
                        content_object=discussion,
                        file=file,
                        uploaded_by=request.user,
                    )
                return redirect("hub_detail", hub_id=hub.id)
    else:
        post_form = PostForm(initial={"hub": hub})
        discussion_form = DiscussionForm(initial={"hub": hub})

    context = {
        "hub": hub,
        "posts": posts,
        "discussions": discussions,
        "post_form": post_form,
        "discussion_form": discussion_form,
        "followed_hubs": followed_hubs,
    }
    return render(request, "hub_detail.html", context)


# Voting Views
@login_required
def upvote_view(request, content_type, object_id):
    content_type_obj = get_object_or_404(ContentType, model=content_type)
    obj = get_object_or_404(content_type_obj.model_class(), id=object_id)
    vote, created = Vote.objects.get_or_create(
        user=request.user,
        content_type=content_type_obj,
        object_id=object_id,
        defaults={"value": 1},
    )
    if not created and vote.value != 1:
        vote.value = 1
        vote.save()
    return redirect(request.META.get("HTTP_REFERER", "success"))


@login_required
def downvote_view(request, content_type, object_id):
    content_type_obj = get_object_or_404(ContentType, model=content_type)
    obj = get_object_or_404(content_type_obj.model_class(), id=object_id)
    vote, created = Vote.objects.get_or_create(
        user=request.user,
        content_type=content_type_obj,
        object_id=object_id,
        defaults={"value": -1},
    )
    if not created and vote.value != -1:
        vote.value = -1
        vote.save()
    return redirect(request.META.get("HTTP_REFERER", "success"))


def get_post_votes(post):
    upvotes = post.votes.filter(value=1).count()
    downvotes = post.votes.filter(value=-1).count()
    return upvotes, downvotes


def get_hub_total_votes(hub):
    from django.db.models import Sum

    agg = hub.posts.aggregate(total=Sum("votes__value"))
    return agg["total"] or 0


def recent_activity_view(request):
    last_hubs = Hub.objects.order_by("-created_at")[:5]
    posts = Post.objects.filter(hub__in=last_hubs).order_by("-created_at")[:20]
    context = {
        "posts": posts,
        "hubs": last_hubs,
        "discussions": Discussion.objects.filter(hub__in=last_hubs).order_by(
            "-created_at"
        )[:5],
    }
    return render(request, "recent_activity.html", context)


@login_required
def create_discussion_view(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    if request.method == "POST":
        form = DiscussionForm(request.POST, request.FILES)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.hub = hub
            discussion.author = request.user
            discussion.save()
            form.save_m2m()
            files = request.FILES.getlist("attachments")
            for file in files:
                Attachment.objects.create(
                    content_object=discussion,
                    file=file,
                    uploaded_by=request.user,
                )
            return redirect("hub_detail", hub_id=hub.id)
    else:
        form = DiscussionForm(initial={"hub": hub})
    return render(request, "create_discussion.html", {"form": form, "hub": hub})


@login_required
def edit_discussion_view(request, pk):
    discussion = get_object_or_404(Discussion, id=pk)
    if request.user != discussion.author:
        return HttpResponseForbidden("You are not allowed to edit this discussion.")
    if request.method == "POST":
        form = DiscussionForm(request.POST, request.FILES, instance=discussion)
        if form.is_valid():
            discussion = form.save()
            files = request.FILES.getlist("attachments")
            for file in files:
                Attachment.objects.create(
                    content_object=discussion,
                    file=file,
                    uploaded_by=request.user,
                )
            return redirect("discussion_detail", pk=discussion.id)
    else:
        form = DiscussionForm(instance=discussion)
    return render(
        request, "edit_discussion.html", {"form": form, "discussion": discussion}
    )


@login_required
def delete_discussion_view(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if discussion.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this discussion.")
    if request.method == "POST":
        hub_id = discussion.hub.id
        discussion.delete()
        return redirect("hub_detail", hub_id=hub_id)
    return render(request, "confirm_action.html", {"obj": discussion})


def discussion_detail_view(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    comments = Comment.objects.filter(discussion=discussion, parent__isnull=True).prefetch_related(
        "replies", "author", "attachments"
    )
    discussion.attachments_with_basename = [
        {"file": attachment.file, "basename": os.path.basename(attachment.file.name)}
        for attachment in discussion.attachments.all()
    ]
    for comment in comments:
        comment.attachments_with_basename = [
            {"file": attachment.file, "basename": os.path.basename(attachment.file.name)}
            for attachment in comment.attachments.all()
        ]
        comment.indentation = (comment.level if hasattr(comment, 'level') else 0) * 20

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.discussion = discussion
            parent_id = request.POST.get("parent")
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            files = request.FILES.getlist("attachments")
            for file in files:
                Attachment.objects.create(
                    content_object=comment,
                    file=file,
                    uploaded_by=request.user,
                )
            return redirect("discussion_detail", pk=discussion.pk)
    else:
        form = CommentForm()

    return render(
        request,
        "discussion_detail.html",
        {"discussion": discussion, "comments": comments, "form": form},
    )

@login_required
def hubs_overview_view(request):
    user_hubs = Hub.objects.filter(author=request.user)
    all_hubs = Hub.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        "user_hubs": user_hubs,
        "all_hubs": all_hubs,
        "categories": categories,
        "tags": tags,
    }
    return render(request, "hubs_overview.html", context)


@login_required
def follow_hub(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    FollowingHub.objects.get_or_create(user=request.user, hub=hub)
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))


@login_required
def unfollow_hub(request, hub_id):
    hub = get_object_or_404(Hub, id=hub_id)
    FollowingHub.objects.filter(user=request.user, hub=hub).delete()
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))


@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        return redirect(request.META.get("HTTP_REFERER", "dashboard"))
    FollowingUser.objects.get_or_create(user=request.user, following_user=target_user)
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))


@login_required
def unfollow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    FollowingUser.objects.filter(user=request.user, following_user=target_user).delete()
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))

@login_required
def unfollow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    FollowingUser.objects.filter(user=request.user, following_user=target_user).delete()
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))

def user_profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_posts = Post.objects.filter(author=user)
    user_hubs = Hub.objects.filter(author=user)
    user_discussions = Discussion.objects.filter(author=user)
    followed_hubs = user.followed_hubs.all()
    followers_count = FollowingUser.objects.filter(following_user=user).count()
    following_count = FollowingUser.objects.filter(user=user).count()
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = FollowingUser.objects.filter(user=request.user, following_user=user).exists()

    context = {
        "user": user,
        "user_posts": user_posts,
        "user_hubs": user_hubs,
        "user_discussions": user_discussions,
        "followed_hubs": followed_hubs,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
        "request": request,
    }
    return render(request, "user_profile.html", context)

def user_posts(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=user)
    return render(request, "user_posts.html", {"user": user, "posts": posts})

def user_hubs(request, user_id):
    user = get_object_or_404(User, id=user_id)
    hubs = Hub.objects.filter(author=user)
    return render(request, "user_hubs.html", {"user": user, "hubs": hubs})

def user_discussions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    discussions = Discussion.objects.filter(author=user)
    return render(request, "user_discussions.html", {"user": user, "discussions": discussions})

def user_comments(request, user_id):
    user = get_object_or_404(User, id=user_id)
    comments = Comment.objects.filter(author=user)
    return render(request, "user_comments.html", {"user": user, "comments": comments})

def user_followed_hubs(request, user_id):
    user = get_object_or_404(User, id=user_id)
    hubs = user.followed_hubs.all()
    return render(request, "user_followed_hubs.html", {"user": user, "hubs": hubs})

def user_followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = FollowingUser.objects.filter(following_user=user)
    return render(request, "user_followers.html", {"user": user, "followers": followers})

def user_following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    following = FollowingUser.objects.filter(user=user)
    return render(request, "user_following.html", {"user": user, "following": following})

@login_required
def following_feed(request):
    following_users = User.objects.filter(followers__user=request.user)
    following_hubs = Hub.objects.filter(followers=request.user)

    posts = Post.objects.filter(author__in=following_users) | Post.objects.filter(hub__in=following_hubs)
    discussions = Discussion.objects.filter(author__in=following_users) | Discussion.objects.filter(hub__in=following_hubs)

    posts = posts.distinct().order_by('-created_at')
    discussions = discussions.distinct().order_by('-created_at')

    return render(request, "following_feed.html", {
        "posts": posts,
        "discussions": discussions,
        "following_users": following_users,
        "following_hubs": following_hubs,
    })

# Public Chat Views
@login_required
def public_chat_create(request):
    if request.method == 'POST':
        form = PublicChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.owner = request.user
            chat.admin = request.user
            chat.save()
            form.save_m2m()  # Save many-to-many fields
            chat.members.add(request.user)  # Add creator as member
            PublicChatRole.objects.create(
                chat=chat,
                user=request.user,
                role_name='Owner',
                permissions={'can_manage_chat': True, 'can_moderate': True}
            )
            if request.is_ajax():
                return JsonResponse({
                    'message': f"Public chat '{chat.title}' created successfully!",
                    'chat_id': chat.id
                })
            messages.success(request, f"Public chat '{chat.title}' created successfully!")
            return redirect('chat:public_chat_list')
        else:
            if request.is_ajax():
                return JsonResponse({'errors': form.errors}, status=400)
            messages.error(request, "Invalid form data.")
    else:
        form = PublicChatForm()
    return render(request, 'chat/public_chat_form.html', {'form': form, 'action': 'Create'})

@login_required
def public_chat_update(request, pk):
    chat = get_object_or_404(PublicChat, pk=pk)
    role = PublicChatRole.objects.filter(chat=chat, user=request.user).first()
    if request.user != chat.owner and not (role and role.permissions.get('can_manage_chat', False)):
        messages.error(request, "You do not have permission to edit this chat.")
        return redirect('chat:public_chat_list')

    if request.method == 'POST':
        form = PublicChatForm(request.POST, instance=chat)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({
                    'message': f"Public chat '{chat.title}' updated successfully!",
                    'chat_id': chat.id
                })
            messages.success(request, f"Public chat '{chat.title}' updated successfully!")
            return redirect('chat:public_chat_list')
        else:
            if request.is_ajax():
                return JsonResponse({'errors': form.errors}, status=400)
            messages.error(request, "Invalid form data.")
    else:
        form = PublicChatForm(instance=chat)
    return render(request, 'chat/public_chat_form.html', {'form': form, 'action': 'Update'})

@login_required
def public_chat_delete(request, pk):
    chat = get_object_or_404(PublicChat, pk=pk)
    if request.user != chat.owner:
        messages.error(request, "Only the owner can delete this chat.")
        return redirect('chat:public_chat_list')

    if request.method == 'POST':
        title = chat.title
        chat.delete()
        if request.is_ajax():
            return JsonResponse({'message': f"Public chat '{title}' deleted successfully!"})
        messages.success(request, f"Public chat '{title}' deleted successfully!")
        return redirect('chat:public_chat_list')
    return render(request, 'chat/public_chat_confirm_delete.html', {'chat': chat})

@login_required
def public_chat_detail(request, pk):
    chat = get_object_or_404(PublicChat, pk=pk)
    messages = chat.messages.order_by('created_at')[:50]  # Load recent 50 messages
    form = MessageForm(initial={'chat': chat})
    is_member = chat.members.filter(id=request.user.id).exists()
    role = PublicChatRole.objects.filter(chat=chat, user=request.user).first()
    context = {
        'chat': chat,
        'messages': messages,
        'form': form,
        'is_member': is_member,
        'role': role
    }
    return render(request, 'chat/public_chat_detail.html', context)

# Message Views
@login_required
def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            try:
                message.full_clean()  # Validate the message
                message.save()
                # Handle file attachments
                files = request.FILES.getlist('attachments')
                for file in files:
                    attachment = Attachment.objects.create(file=file, uploaded_by=request.user)
                    message.files.add(attachment)
                if request.is_ajax():
                    return JsonResponse({
                        'id': message.id,
                        'content': message.content,
                        'author': message.author.username,
                        'created_at': message.created_at.isoformat(),
                        'chat_type': 'PublicChat' if message.chat else 'PrivateChat'
                    })
                messages.success(request, "Message sent successfully!")
                return redirect('chat:public_chat_detail', pk=message.chat.id if message.chat else message.private_chat.id)
            except ValidationError as e:
                if request.is_ajax():
                    return JsonResponse({'errors': str(e)}, status=400)
                messages.error(request, str(e))
        else:
            if request.is_ajax():
                return JsonResponse({'errors': form.errors}, status=400)
            messages.error(request, "Invalid message data.")
    return HttpResponseBadRequest("Invalid request method.")

@login_required
def message_update(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.author != request.user:
        messages.error(request, "You can only edit your own messages.")
        return redirect('chat:public_chat_detail', pk=message.chat.id if message.chat else message.private_chat.id)

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            message = form.save()
            if request.is_ajax():
                return JsonResponse({
                    'message': "Message updated successfully!",
                    'id': message.id,
                    'content': message.content
                })
            messages.success(request, "Message updated successfully!")
            return redirect('chat:public_chat_detail', pk=message.chat.id if message.chat else message.private_chat.id)
        else:
            if request.is_ajax():
                return JsonResponse({'errors': form.errors}, status=400)
            messages.error(request, "Invalid form data.")
    else:
        form = MessageForm(instance=message)
    return render(request, 'chat/message_form.html', {'form': form, 'message': message})

@login_required
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    role = PublicChatRole.objects.filter(chat=message.chat, user=request.user).first() if message.chat else None
    if message.author != request.user and not (role and role.permissions.get('can_moderate', False)):
        messages.error(request, "You do not have permission to delete this message.")
        return redirect('chat:public_chat_detail', pk=message.chat.id if message.chat else message.private_chat.id)

    if request.method == 'POST':
        chat_id = message.chat.id if message.chat else message.private_chat.id
        message.delete()
        if request.is_ajax():
            return JsonResponse({'message': "Message deleted successfully!"})
        messages.success(request, "Message deleted successfully!")
        return redirect('chat:public_chat_detail', pk=chat_id)
    return render(request, 'chat/message_confirm_delete.html', {'message': message})

# Private Chat Views
@login_required
def private_chat_create(request):
    if request.method == 'POST':
        form = PrivateChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.user1 = request.user
            try:
                chat.full_clean()  # Validate the chat
                chat.save()
                if request.is_ajax():
                    return JsonResponse({
                        'message': "Private chat created successfully!",
                        'chat_id': chat.id
                    })
                messages.success(request, "Private chat created successfully!")
                return redirect('chat:private_chat_list')
            except ValidationError as e:
                if request.is_ajax():
                    return JsonResponse({'errors': str(e)}, status=400)
                messages.error(request, str(e))
        else:
            if request.is_ajax():
                return JsonResponse({'errors': form.errors}, status=400)
            messages.error(request, "Invalid form data.")
    else:
        form = PrivateChatForm()
    return render(request, 'chat/private_chat_form.html', {'form': form})

@login_required
def private_chat_delete(request, pk):
    chat = get_object_or_404(PrivateChat, pk=pk)
    if request.user not in [chat.user1, chat.user2]:
        messages.error(request, "You do not have permission to delete this chat.")
        return redirect('chat:private_chat_list')

    if request.method == 'POST':
        chat.delete()
        if request.is_ajax():
            return JsonResponse({'message': "Private chat deleted semessage_confirm_delete.htmluccessfully!"})
        messages.success(request, "Private chat deleted successfully!")
        return redirect('chat:private_chat_list')
    return render(request, 'chat/private_chat_confirm_delete.html', {'chat': chat})

# List Views
@login_required
def public_chat_list(request):
    chats = PublicChat.objects.filter(Q(members=request.user) | Q(owner=request.user)).distinct()
    return render(request, 'chat/public_chat_list.html', {'chats': chats})

@login_required
def private_chat_list(request):
    chats = PrivateChat.objects.filter(Q(user1=request.user) | Q(user2=request.user)).distinct()
    return render(request, 'chat/private_chat_list.html', {'chats': chats})
