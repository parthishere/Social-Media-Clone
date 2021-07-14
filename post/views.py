from django.shortcuts import render, reverse, redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import permission_required, login_required

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
    return render(request, "post_list.html", context={'post':post, 'pk':pk})
    
    
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


@login_required
def save_post_view(request, pk=None):
    post = Post.objects.get(pk=pk)
    user_profile=request.user.user_profile

    if post in user_profile.saved_posts.all():
        user_profile.saved_posts.remove(post)
    else:
        user_profile.saved_posts.add(post)

    user_profile.save()
    return redirect('post:list')

@login_required
def saved_posts_list_view(request):
    user = request.user
    user_profile = user.user_profile
    context = {}

    post_list = user_profile.saved_posts.all()
    
    context['objects_list'] = post_list
    return render(request, 'post_list.html', context=context)