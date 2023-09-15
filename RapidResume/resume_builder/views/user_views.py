from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View

from ..forms import UserProfileForm
from ..models import UserProfile

class UserProfileView(LoginRequiredMixin, View):
    
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)  # Get or create a profile for the logged-in user
        form = UserProfileForm(instance=profile)

        # Check if profile is empty
        is_empty = not profile.contact_number and not profile.address

        if is_empty or request.GET.get('edit') == 'true':
            return render(request, 'resume_builder/user_profile_form.html', {'form' : form})    
        else:
            return render(request, 'resume_builder/user_profile_display.html', {'profile' : profile})

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('user_profile')
        
        return render(request, 'resume_builder/user_profile_form.html', {'form' : form})


