from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    template_name = 'index.html'
    context = {}
    return render(request, template_name, context)