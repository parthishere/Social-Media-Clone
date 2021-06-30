from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db.models import Q


from .models import User, UserProfile, TopicTag
# Create your views here.

class UserProfileDetailView(View):
    template_name = "accounts/user_profile.html"
    
    def get(self, request):
        context = {}
        user = request.user
        user_profile = request.user.user_profile
        context['user'] = user
        context['user_profile'] = user_profile
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
            context['object_list'] = UserProfile.objects.filter(obj_list).distinct()
            context['query'] = query
            return context
        else:
            return UserProfile.objects.all().order_by('followers_count')[0:5]
    

class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/update_profile_form.html'
    form_class = UserUpdateForm
    success_url = '/home/'
    
    def get_success_url(self):
        next_url = self.request.data.get('next_url')
        if next_url is not None:
            return reverse(next_url)
        else: 
            return self.success_url