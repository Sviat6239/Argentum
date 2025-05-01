from django import forms
from .models import Post, Comment, Hub, Tag, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['hub', 'category', 'tag','title', 'content', 'author', 'created_at']

        labels = {
            'hub': 'Hub',
            'category': 'Category',
            'tag': 'Tag',
            'title': 'Title',
            'content':'Content',
            'author': 'Author',
            'created_at':'Created At'
        }

        widgets = {
            'hub': forms.Select(),
            'category': forms.Select(),
            'tag': forms.Select(),
            'title' : forms.TextInput(attrs={'placeholder': 'eg. A one day...'}),
            'content' : forms.Textarea(attrs={'placeholder': 'eg. I saw a black cat...'}),
            'author': forms.Select(),
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'readonly': True}),

        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post','content', 'author', 'created_at']

        labels = {
            'post': 'Post', 
            'content': 'Content',
            'author': 'Author', 
            'created_at': 'Created At'
        }        

        widgwts = {
            'post': forms.Select(),
            'content':forms.Textarea(attrs={'Placeholder': 'eg. Nice post!'}),
            'author': forms.Select(),
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'readonly': True}),
        }

class HubForm(forms.ModelForm):
    class Meta:
        model = Hub  

        fields = ['title', 'description', 'author', 'created_at']

        labels = {
            'title': 'Title',
            'description': 'Description',
            'author': 'Author',
            'created_at': 'Created At'
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'eg. Nice hub!'}),
            'description': forms.Textarea(attrs={'placeholder': 'eg. Join our hub'}),
            'author': forms.Select(),
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'readonly': True}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category

        fields = ['title']

        labels = {
            'title': 'Title'
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'eg. Nice category!'})
        }

class TagForm(forms.ModelForm):
    class Meta:
        models = Tag

        fields = ['title'] 

        labels = {
            'title': 'Title'
        }       

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'eg. Nice tag!'})
        }

      