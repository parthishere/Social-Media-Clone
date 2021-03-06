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
    queryset = UserProfile.objects.all()
    template_name = "accounts/user_profile.html"
    
    def get(self, request, username=None):
        context = {}
        user_profile = UserProfile.objects.get(user__username=username)
        user = user_profile.user
        context['user'] = user
        context['user_profile'] = user_profile
        if request.user.is_authenticated and user_profile.private_account:
            if request.user in user_profile.followers.all():
                context['posts'] = user.post_user.all()
            else:
                context['posts'] = None
        elif not request.user.is_authenticated and user_profile.private_account:
            context['posts'] = None
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
                Q(followers__username__in=query) 
            )
            context['objects_list'] = UserProfile.objects.filter(obj_list).order_by('-followers_count').distinct()
            context['query'] = query
            return context
        else:
            context['objects_list'] = UserProfile.objects.all().order_by('-followers_count')
            return context
    

class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    queryset = UserProfile.objects.all()
    template_name = 'accounts/update_profile_form.html'
    form_class = UserProfileForm
    model = UserProfile
    success_url = '/list/'
    slug_field = 'user__username'
    slug_url_kwarg = 'user__username'
    lookup_field = ['user__username']
    
    
    # def form_validate(self, form):
    #     if form.instance.email is not None:
            
    def get_success_url(self):
        next_url = self.request.data.get('next_url')
        if next_url is not None:
            return reverse(next_url)
        else: 
            return self.success_url
        
        
        
def user_profile_update(request, username=None):
    user_profile = UserProfile.objects.get(user__username=username)
    form = UserProfileForm(request.POST or None, instance=user_profile)
    
    context = { 'form': form, }
    
    if request.POST:
        if form.is_valid():
            form.save()
            context['form'] = form    
            return redirect(reverse('accounts:profile', kwargs={'username':request.user.username}))
    else:
        form = UserProfileForm(request.POST or None, instance=user_profile)
        context['form'] = form

    return render(request, 'accounts/update_profile_form.html', context=context)
    
    
    
def user_followers_list(request, username=None):
    user_profile = UserProfile.objects.get(user__username=username)
    user = user_profile.user
    context = {}
    
    followers_qs = user_profile.followers.all()
    followers_count = user_profile.followers_count
    

    context['objects_list'] = followers_qs ## User Object
    context['count'] = followers_count
    
    return render(request, 'accounts/followers_list.html', context=context)


def user_following_list(request, username=None):
    context = {}
    user_profile = UserProfile.objects.get(user__username=username)
    user = user_profile.user

    following_qs = user.following.all().prefetch_related('user')
    following_count = user_profile.following_count
    
    context['objects_list'] = following_qs # User Object
    context['count'] = following_count
    return render(request, 'accounts/following_list.html', context=context)



def remove_follower_view(request, username=None):
    user = request.user
    user_profile = user.user_profile
    
    remove_user_profile = UserProfile.objects.get(user__username=username)
    
    if remove_user_profile.user in user_profile.followers.all():
        user_profile.followers.remove(remove_user_profile.user)
        
        print('working')

    else:
        print('not workking')
    
    user_profile.save()
    return redirect(reverse('accounts:user-followers', kwargs={"username":user.username}))


def remove_following_view(request, username=None):
    user = request.user
    user_profile = user.user_profile
    
    unfollow_user_profile = UserProfile.objects.get(user__username=username)
    
    if user_profile.user in unfollow_user_profile.followers.all():
        unfollow_user_profile.followers.remove(user)
    else:
        pass
    
    user_profile.save()
    return redirect(reverse('accounts:profile', kwargs={"username":unfollow_user_profile.user.username}))



def follow_unfollow_requested_user(request, username=None):
    if request.user.is_authenticated:
        user= request.user
        user_profile = user.user_profile

        requested_user_profile = UserProfile.objects.get(user__username=username)
        requested_user = requested_user_profile.user

        if requested_user_profile.private_account:
            if user in requested_user_profile.followers.all():
                requested_user_profile.followers.remove(user)
                if user in requested_user_profile.followers_requests.all():
                    requested_user_profile.followers_requests.remove(user)
            else:
                requested_user_profile.followers_requests.add(user)
                
        else:
            if user not in requested_user_profile.followers.all():
                requested_user_profile.followers.add(user)
                # requested_user_profile.followers_count = requested_user_profile.followers.all().count()
                
            else:
                requested_user_profile.followers.remove(user)
               
        requested_user_profile.save()     
    return redirect(reverse('accounts:profile', kwargs={'username':requested_user.username}))



def follow_requested_user_list(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = user.user_profile

        context = {}
        if user_profile.private_account:
            context['objects_list'] = user_profile.followers_requests.all()
        else:
            context = {}
            
        
            
        return render(request, 'accounts/follow_requests.html', context=context)
    
    
def accept_follow_request_view(request, username=None):
    if request.user.is_authenticated:
        user = request.user
        user_profile = user.user_profile
        
        requested_follower_profile = UserProfile.objects.get(user__username=username)
        requested_follower = requested_follower_profile.user

        if requested_follower in user_profile.followers.all():
            if requested_follower in user_profile.followers_requests.all():
                user_profile.followers_requests.remove(requested_follower)
        elif requested_follower in user_profile.followers_requests.all():
            user_profile.followers_requests.remove(requested_follower)
            user_profile.followers.add(requested_follower)
            
        user_profile.save()
        return redirect(reverse('accounts:followers-requests'))
    else:
        return redirect('login')
   
def decline_follow_request_view(request, username=None):
    if request.user.is_authenticated:
        user = request.user
        user_profile = user.user_profile
        
        requested_follower_profile = UserProfile.objects.get(user__username=username)
        requested_follower = requested_follower_profile.user

        if requested_follower in user_profile.followers.all():
            if requested_follower in user_profile.followers_requests.all():
                user_profile.followers_requests.remove(requested_follower)
        elif requested_follower in user_profile.followers_requests.all():
            user_profile.followers_requests.remove(requested_follower)
            
        user_profile.save()
        return redirect(reverse('accounts:followers-requests'))
    else:
        return redirect('login') 


def change_profile_type_view(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = user.user_profile 
        
        if user_profile.private_account:
            user_profile.private_account = False
            user_profile.followers.add(
                user for user in user_profile.followers_requests.all()
            )
            user_profile.followers_requests.clear()
            user_profile.save()
        else:
            user_profile.private_account = True        
            
        user_profile.save()
        return redirect(reverse('accounts:profile', kwargs={'username':user.username}))   


# def follow_unfollow_requested_user(request, username=None):
#     user= request.user
#     user_profile = user.user_profile

#     requested_user_profile = UserProfile.objects.get(user__username=username)
#     requested_user = requested_user_profile.user

    
#     if user not in requested_user_profile.followers.all():
#         requested_user_profile.followers.add(user)
#         # requested_user_profile.followers_count = requested_user_profile.followers.all().count()
#         requested_user_profile.save()
#     else:
#         requested_user_profile.followers.remove(user)
#         requested_user_profile.save()
        
#     return redirect(reverse('accounts:profile', kwargs={'username':requested_user.username}))

# def report_account(request, username=None):
#     user= request.user
#     user_profile = user.user_profile

#     requested_user_profile = UserProfile.objects.get(user__username=username)
#     requested_user = requested_user_profile.user

    
#     if user not in requested_user_profile.reported_by.all():
#         requested_user_profile.followers.add(user)
#         # requested_user_profile.followers_count = requested_user_profile.followers.all().count()
#         requested_user_profile.save()
#     else:
#         requested_user_profile.followers.remove(user)
#         requested_user_profile.save()
        
#     return redirect(reverse('accounts:profile', kwargs={'username':user_profile.username}))