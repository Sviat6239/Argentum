from django import forms
from autentification.models import CustomUser
from .models import UserProfile
from blog.models import Post, Comment, Hub

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['name', 'post', 'comment', 'hub']
        labels = {
            'name': 'Display Name',
            'post': 'Associated Post',
            'comment': 'Associated Comment',
            'hub': 'Associated Hub',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your display name'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['post'].queryset = Post.objects.filter(author=user)
            self.fields['comment'].queryset = Comment.objects.filter(author=user)
            self.fields['hub'].queryset = Hub.objects.filter(owner=user)
        self.fields['post'].required = False
        self.fields['comment'].required = False
        self.fields['hub'].required = False

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = user_profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.bio = self.cleaned_data['bio']
        if self.cleaned_data['profile_picture']:
            user.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            user.save()
            user_profile.save()
        return user_profile