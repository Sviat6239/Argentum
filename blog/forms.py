from django import forms
from .models import Post, Comment, Hub, Category, Tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['hub', 'category', 'tags', 'title', 'content']

        labels = {
            'hub': 'Hub',
            'category': 'Category',
            'tags': 'Tags',
            'title': 'Title',
            'content': 'Content',
        }

        widgets = {
            'hub': forms.Select(),
            'category': forms.Select(),
            'tags': forms.SelectMultiple(),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. A one day...'}),
            'content': forms.Textarea(attrs={'placeholder': 'e.g. I saw a black cat...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [#'post',
                   'content']

        labels = {
            #'post': 'Post',
            'content': 'Content',
        }

        widgets = {
            #'post': forms.Select(),
            'content': forms.Textarea(attrs={'placeholder': 'e.g. Nice post!'}),
        }

class HubForm(forms.ModelForm):
    class Meta:
        model = Hub
        fields = ['title', 'description']

        labels = {
            'title': 'Title',
            'description': 'Description',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Nice hub!'}),
            'description': forms.Textarea(attrs={'placeholder': 'e.g. Join our hub'}),
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