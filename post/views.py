from django.shortcuts import render, reverse, redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Post
from .forms import PostForm

# Create your views here.

class PostListView(ListView):
    queryset = Post.objects.all()
    model = Post
    template_name = 'post/post_list.html'
   
    
def like_post_view(request):
    pk = request.data.get('post_pk')
    post = Post.objects.filter(pk=pk)
    if post.exists and pk is not None:
        if request.POST:
            if request.user in post.liked_user.all():
                post.liked_user.remove(request.user)
                post.like_count = post.liked_user.all().count()
            else:
                post.liked_user.add(request.user)
                post.like_count = post.liked_user.all().count()
            post.save()
            return redirect('post:list')
    return render(request, "", context={})
    
    
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    queryset = Post.objects.all()
    template_name = 'post/post_form.html'
    slug_field = 'pk'
    lookup_field = ['pk',]
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
     
        
class PostCreateView(UpdateView):
    model = Post
    form_class = PostForm
    queryset = Post.objects.all()
    template_name = 'post/post_form.html'
    slug_field = 'pk'
    lookup_field = ['pk',]
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def save_post_view(request, pk=None):
    return render(request, '', context={})