from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse


# Create your views here.
from account.models import Profile


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        exist = User.objects.filter(username=username).first()
        if password != confirm_password:
            messages.error(request, 'Password unmatched')
            return redirect('home')
        if exist:
            messages.error(request, 'Username already exists')
            return redirect('home')
        exist = User.objects.filter(email=email).first()
        if exist:
            messages.error(request, 'Email already exists')
            return redirect('home')
        User.objects.create_user(username=username, password=password, email=email)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            Profile.objects.create(user=user, role="student")
            messages.success(request, 'Account created successful')
            return redirect('home')
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
        else:
            messages.error(request, 'Username and password unmatched')
            return redirect('home')
    return redirect('home')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('home')


def profile(request):
    if request.method == 'POST':
        profile = Profile.objects.filter(user=request.user).first()
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.bio = request.POST.get('bio')
        profile.cover = request.FILES.get('cover')
        profile.save()
        messages.success(request, 'Profile updated successful')
        return redirect('profile')
    user = User.objects.filter(id=request.GET.get('user_id')).first()
    try:
        user.profile
    except:
        Profile.objects.create(user=user)
    context={
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'bio':user.profile.bio,
        'photo':user.profile.cover.url if user.profile.cover else None,
        'role':user.profile.role,
        'restaurant':user.profile.restaurant,
    }
    return render(request, 'accounts/profile.html', context)

def update_profile(request):
    if request.method == 'POST':
        profile = Profile.objects.filter(user=request.user).first()
        profile.user.first_name = request.POST.get('first_name')
        profile.user.last_name = request.POST.get('last_name')
        profile.user.email = request.POST.get('email')
        profile.bio = request.POST.get('bio')
        profile.user.save()
        profile.cover = request.FILES.get('cover', profile.cover)
        profile.save()
        messages.success(request, 'Profile updated successful')
        return redirect(reverse('profile')+'?user_id='+str(profile.user.id))
    user = User.objects.filter(id=request.user.id).first()
    context={
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'photo':user.profile.cover.url if user.profile.cover else None,
        'role':user.profile.role,
        'bio':user.profile.bio,
        'restaurant':user.profile.restaurant,
    }
    return render(request, 'accounts/update_profile.html', context)