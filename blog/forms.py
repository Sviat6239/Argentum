from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['id','title', 'content', 'author', 'created_at']

        labels = {
            'id': 'ID',
            'title':'Title',
            'content':'Content',
            'author': 'Author',
            'created_at':'Created At'
        }

        widgets = {
            'id' : forms.NumberInput(attrs={'placeholder': 'eg. 101'}),
            'title' : forms.TextInput(attrs={'placeholder': 'eg. A one day...'}),
            'content' : forms.Textarea(attrs={'placeholder': 'eg. I saw a black cat...'}),
            'author': forms.Select(),
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})

        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']

        labels = {
            'id': 'ID', 
            'content': 'Content',
            'author': 'Author', 
            'created_at': 'Created At'
        }        

        widgwts = {
            'id': forms.NumberInput(attrs={'placeholder': 'eg. 501'}),
            'content':forms.TextArea(attrs={'Placeholder': 'eg. Nice post!'}),
            'author': forms.Select(),
            'created_at': forms.DateTimeInput(atrrs={'type': 'datetime-local'}),
        }