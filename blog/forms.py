from django import forms
from .models import Discussion, Post, Comment, Hub, Category, Tag, UserProfile

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

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['hub', 'category', 'tags', 'title', 'content', 'post', 'comment', 'parent_discussion']
        labels = {
            'hub': 'Hub',
            'category': 'Category',
            'tags': 'Tags',
            'title': 'Discussion Title',
            'content': 'Content',
            'post': 'Associated Post',
            'comment': 'Associated Comment',
            'parent_discussion': 'Parent Discussion',
        }
        widgets = {
            'hub': forms.Select(),
            'category': forms.Select(),
            'tags': forms.SelectMultiple(),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Let’s discuss this topic...'}),
            'content': forms.Textarea(attrs={'placeholder': 'e.g. Share your thoughts here...', 'rows': 5, 'cols': 40}),
            'post': forms.Select(),
            'comment': forms.Select(),
            'parent_discussion': forms.Select(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['post'].queryset = Post.objects.filter(author=user)
            self.fields['comment'].queryset = Comment.objects.filter(author=user)
            self.fields['parent_discussion'].queryset = Discussion.objects.filter(author=user)
            if self.instance and self.instance.pk:
                self.fields['parent_discussion'].queryset = self.fields['parent_discussion'].queryset.exclude(pk=self.instance.pk)
            self.fields['hub'].queryset = Hub.objects.filter(author=user)
            if self.instance and self.instance.hub:
                self.fields['category'].queryset = self.instance.hub.categories.all()
            elif 'initial' in kwargs and 'hub' in kwargs['initial']:
                hub = kwargs['initial']['hub']
                self.fields['category'].queryset = hub.categories.all()
            else:
                self.fields['category'].queryset = Category.objects.all()
        self.fields['post'].required = False
        self.fields['comment'].required = False
        self.fields['parent_discussion'].required = False
        self.fields['tags'].required = False

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['name']
        labels = {'name': 'Display Name'}
        widgets = {'name': forms.TextInput(attrs={'placeholder': 'Enter your display name'})}

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