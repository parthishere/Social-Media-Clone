from django.shortcuts import render, reverse, redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Post

# Create your views here.
class PostListView(ListView):
    queryset = Post.objects.all()