from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import permission_required, login_required

from .models import Comment
from .forms import CommentForm

# Create your views here.
class CommentListView(View):
    pass    
    
    
def like_comment_view(request):
    context = {}
    if request.POST:
        pk = request.POST.get('post_pk')
        post = Comment.objects.get(pk=pk)
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
    
    
# class CommentUpdateView(UpdateView):
#     model = Comment
#     form_class = CommentForm
#     queryset = Comment.objects.all()
#     template_name = 'post/post_form.html'
#     slug_field = 'pk'
    
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         if self.request.POST.get('parent'):
#             form.instance.parent = self.request.POST.get('parent')
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return reverse_lazy('profiles:detail', kwargs={'slug': self.slug})
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['url'] = reverse('post:update', kwargs={'pk':self.instance.pk})
#         return context
     
        
class CommentCreateView(CreateView):
    model = Comment
    form_class = Comment
    template_name = 'post/post_form.html'
    
    def form_valid(self, form):   
        comment = form.save(commit=False)
        parent = self.request.POST.get('parent')
        if parent is not None:
            comment.parent = parent
        comment.user = self.request.user
        comment.save()
        return HttpResponseRedirect(self.get_success_url())
    
    
    def get_success_url(self):
        return reverse('post:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = reverse('post:create')
        return context


class DeleteCommentView(DeleteView):
    model = Comment
    queryset = Comment.objects.all()
    success_url = reverse_lazy('post:list')