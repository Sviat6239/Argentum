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
            'content': forms.Textarea(attrs={'placeholder': 'e.g. Nice post!'}),
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
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Nice hub!'}),
            'description': forms.Textarea(attrs={'placeholder': 'e.g. Join our hub'}),
            'categories': forms.SelectMultiple(),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        labels = {
            'title': 'Title',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Nice category!'}),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
        labels = {
            'title': 'Title',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Nice tag!'}),
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['tags', 'title', 'content']

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content']

    