from django import forms
from .models import Post, Comment, Hub, Category, Tag, Discussion

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Content',
        }
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'e.g. Nice post!', 'rows': 4, 'class': 'form-control'}),
        }

class HubForm(forms.ModelForm):
    class Meta:
        model = Hub
        fields = ['title', 'description', 'categories']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'categories': 'Categories',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Nice hub!', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'e.g. Join our hub', 'rows': 6, 'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'size': 5, 'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        labels = {
            'title': 'Title',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Nice category!', 'class': 'form-control'}),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': 'Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Nice tag!', 'class': 'form-control'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['tags', 'title', 'content']  # Added hub
        labels = {
            'tags': 'Tags',
            'title': 'Title',
            'content': 'Content',
        }
        widgets = {
            'tags': forms.SelectMultiple(attrs={'size': 5, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Nice post!', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'e.g. Write your post here...', 'rows': 6, 'class': 'form-control'}),
        }

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['tag', 'title', 'content']  # Added hub
        labels = {
            'tag': 'Tags',
            'title': 'Title',
            'content': 'Content',
        }
        widgets = {
            'tag': forms.SelectMultiple(attrs={'size': 5, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Nice discussion!', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'e.g. Write your discussion here...', 'rows': 6, 'class': 'form-control'}),
        }