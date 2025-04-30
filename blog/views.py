from django.shortcuts import redirect, render
from .forms import PostForm, CommentForm
from .models import Post, Comment


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

def UpdatePostView(request, f_oid):
    obj = Post.objects.get(oid= f_oid)
    form = PostForm(instance=obj)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('index')
        template_name = 'update_post.html'
        context = {'form': form}
        return render(request, template_name, context)
    
def DeleteView(request, f_oid):
    obj = Post.object.get(oid= f_oid)
    if request.method == 'POST':
        obj.delete()
        return redirect('index')
    template_name = 'confirm_delete.html'
    context = {'obj': obj}
    return render(request, template_name, context)