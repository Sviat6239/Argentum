from django import forms
from .models import Post, Comment, Hub, Category, Tag, Discussion, PublicChat, PrivateChat, Message, Attachment

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):
    attachments = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "e.g. Nice post!",
                    "rows": 4,
                    "class": "form-control",
                }
            ),
        }


class HubForm(forms.ModelForm):
    class Meta:
        model = Hub
        fields = ["title", "description", "categories"]
        labels = {
            "title": "Title",
            "description": "Description",
            "categories": "Categories",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. Nice hub!", "class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "e.g. Join our hub",
                    "rows": 6,
                    "class": "form-control",
                }
            ),
            "categories": forms.SelectMultiple(
                attrs={"size": 5, "class": "form-control"}
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title"]
        labels = {"title": "Title"}
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. Nice category!", "class": "form-control"}
            ),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
        labels = {"name": "Name"}
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "e.g. Nice tag!", "class": "form-control"}
            ),
        }


class PostForm(forms.ModelForm):
    attachments = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Post
        fields = ["tags", "title", "content"]
        widgets = {
            "tags": forms.SelectMultiple(
                attrs={"size": 5, "class": "form-control"}
            ),
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. Nice post!", "class": "form-control"}
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "e.g. Write your post here...",
                    "rows": 6,
                    "class": "form-control",
                }
            ),
        }


class DiscussionForm(forms.ModelForm):
    attachments = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Discussion
        fields = ["tags", "title", "content"]
        widgets = {
            "tags": forms.SelectMultiple(
                attrs={"size": 5, "class": "form-control"}
            ),
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. Nice discussion!", "class": "form-control"}
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "e.g. Write your discussion here...",
                    "rows": 6,
                    "class": "form-control",
                }
            ),
        }


class PublicChatForm(forms.ModelForm):
    class Meta:
        model = PublicChat
        fields = ['title', 'description', 'tags', 'hub', 'owner', 'admin', 'moderators', 'members']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'hub': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'admin': forms.Select(attrs={'class': 'form-control'}),
            'moderators': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class PrivateChatForm(forms.ModelForm):
    class Meta:
        model = PrivateChat
        fields = ['user1', 'user2']
        widgets = {
            'user1': forms.Select(attrs={'class': 'form-control'}),
            'user2': forms.Select(attrs={'class': 'form-control'}),
        }


class MessageForm(forms.ModelForm):
    attachments = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=False
    )
    reply_to = forms.ModelChoiceField(
        queryset=Message.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Reply to a specific message (optional)"
    )

    class Meta:
        model = Message
        fields = ['chat', 'private_chat', 'content', 'reply_to']
        widgets = {
            'chat': forms.Select(attrs={'class': 'form-control'}),
            'private_chat': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
