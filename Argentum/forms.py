from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'post', 'comment', 'hub', 'name', 'fname', 'lname', 'bio']
        labels = {
            'id': 'ID',
            'user': 'User',
            'post': 'Post',
            'comment': 'Comment',
            'hub': 'Hub',
            'name': 'Name',
            'fname': 'First Name',
            'lname': 'Last Name',
            'bio': 'Biography'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'fname': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'lname': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
        }