from django.shortcuts import redirect, render
from .forms import PostForm, CommentForm
from .models import Post, Comment

#Post CRUD
def CreatePostView(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        template_name = 'create_post.html'
        context = {'form': form}
    return render(request, template_name, context)

def ShowPostView(request):
    obj = Post.objects.all()
    template_name = 'view_post.html'
    context = {'obj': obj}
    return render(request, template_name, context)

def UpdatePostView(request, f_id):
    obj = Post.objects.get(id= f_id)
    form = PostForm(instance=obj)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('index')
        template_name = 'update_post.html'
        context = {'form': form}
    return render(request, template_name, context)
    
def DeletePostView(request, f_id):
    obj = Post.objects.get(id= f_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('index')
    template_name = 'confirm_delete.html'
    context = {'obj': obj}
    return render(request, template_name, context)

#Comment Crud
def CreateCommentVIew(request):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        template_name = 'create_comment.html'
        context = {'form': form}
    return render(request, template_name, context)
    
def ShowCommentView(request):
    obj = Post.objects.all()
    template_name = "view_comment.html"
    context = {'obl': obj}
    return render(request, template_name, context)

def UpdateCommentView(request, f_id):
    obj = Comment.objects.get(id = f_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('index')
        template_name = 'update_comment.html'
        context = {'form': form}
    return render(request, template_name, context)
    
def DeleteCommentView(request, f_id):
    obj = Comment.objects.get(id=f_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('index')
    template_name = 'confirm_delete.html'
    context = {'obj': obj}
    return render(request, template_name, context)  