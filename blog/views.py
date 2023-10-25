from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

class PostList(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pk'