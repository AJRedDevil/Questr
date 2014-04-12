from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

# Create your views here.
def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('index')
    
def login(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('profile')
    return render(request, 'user/signup.html', locals())

@login_required
def profile(request):
    """Login complete view, displays user data"""
    user = request.user
    return render(request,'user/profile.html', locals())