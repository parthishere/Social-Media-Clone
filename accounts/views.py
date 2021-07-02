from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


from .models import User, UserProfile, TopicTag
from .forms import UserProfileForm
# Create your views here.

class UserProfileDetailView(View):
    template_name = "accounts/user_profile.html"
    
    def get(self, request):
        context = {}
        user = request.user
        user_profile = request.user.user_profile
        context['user'] = user
        context['user_profile'] = user_profile
        context['posts'] = user.post.all()
        return render(request, self.template_name, context=context)
        
        

class UserSearchListView(ListView):
    model = UserProfile
    template_name = 'accounts/user_list.html'
    
    def get_queryset(self, **kwargs):
        return UserProfile.objects.all()
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        request = self.request
        query = request.GET.get('q')
        user_profiles = UserProfile.objects.all()
        if query is not None:
            obj_list = (
                Q(user__username__icontains=query) | Q(bio__icontains=query) | Q(user__first_name__icontains=query) | 
                Q(followers__username__in=query) |Q(user__following__username=query)
            )
            context['objects_list'] = UserProfile.objects.filter(obj_list).distinct()
            context['query'] = query
            return context
        else:
            context['objects_list'] = UserProfile.objects.all().order_by('followers_count')[0:5]
            return context
    

class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/update_profile_form.html'
    form_class = UserProfileForm
    success_url = '/home/'
    
    # def form_validate(self, form):
    #     if form.instance.email is not None:
            
    
    def get_success_url(self):
        next_url = self.request.data.get('next_url')
        if next_url is not None:
            return reverse(next_url)
        else: 
            return self.success_url
    
    
def user_followers_list(request, username=None):
    user_profile = UserProfile.objects.get(user__username=username)
    user = user_profile.user
    context = {}
    
    followers_qs = user_profile.followers.all()
    followers_count = user_profile.followers_count

    context['objects_list'] = followers_qs
    context['count'] = followers_count
    
    return render(request, 'accounts/followers_list.html', context=context)


def user_following_list(request, username=None):
    context = {}
    user_profile = UserProfile.objects.get(user__username=username)
    user = user_profile.user

    following_qs = user.following.all().prefetch_related('user')
    following_count = user_profile.following_count
    
    context['objcets_list'] = following_qs
    context['count'] = following_count
    return render(request, 'accounts/following_list.html', context=context)