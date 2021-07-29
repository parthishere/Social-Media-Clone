from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import permission_required, login_required

from .models import Post
from .forms import PostForm

# Create your views here.
class PostDetailView(View):
    pass

class PostListView(ListView):
    queryset = Post.objects.all()
    model = Post
    template_name = 'post/post_list.html'
    
    
def like_post_view(request):
    context = {}
    if request.POST:
        pk = request.POST.get('post_pk')
        post = Post.objects.get(pk=pk)
        context['post'] = post
        context['pk'] = pk
        if post is not None and pk is not None:
            if request.POST:
                if request.user in post.likes.all():
                    post.likes.remove(request.user)
                    post.like_count = post.likes.all().count()
                else:
                    post.likes.add(request.user)
                    post.like_count = post.likes.all().count()
                post.save()
                return redirect('post:list')
    return render(request, "post/post_list.html", context=context)
    
    
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    queryset = Post.objects.all()
    template_name = 'post/post_form.html'
    slug_field = 'pk'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('profiles:detail', kwargs={'slug': self.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse('post:update', kwargs={'pk':self.instance.pk})
        return context
     
        
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_form.html'
    
    def form_valid(self, form):   
        post = form.save(commit=False)
        img = form.cleaned_data.get('image')
        post.user = self.request.user
        post.image = img
        post.save()
        return HttpResponseRedirect(self.get_success_url())
    
    
    def get_success_url(self):
        return reverse('post:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse('post:create')
        return context


class DeletePostView(DeleteView):
    model = Post
    queryset = Post.objects.all()
    success_url = reverse_lazy('post:list')
    
        

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
    saved_post = user_profile.saved_posts.all()
    context = {}
    context['object_list'] = saved_post

    post_list = user_profile.saved_posts.all()
    
    context['objects_list'] = post_list
    return render(request, 'post/post_list.html', context=context)