from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth.decorators import login_required

# User login view
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    return render(request, 'login.html')

# User logout view
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')  # Redirect to the homepage after logout

# User registration view
def register_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after successful registration
            messages.success(request, 'Account created successfully!')
            return redirect('index')  # Redirect to homepage or any other page after registration
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})

# Update user details (e.g., first_name, last_name, etc.)
@login_required
def update_user(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your details have been updated.')
            return redirect('index')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'update_user.html', {'form': form})

# Change user password view
@login_required
def update_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been updated.')
            return redirect('index')  # Redirect to the homepage or any other page after password change
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'update_password.html', {'form': form})

# Update additional user info like phone, address, etc.
@login_required
def update_info(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile information has been updated.')
            return redirect('index')  # Redirect to the homepage or profile page after info update
    else:
        form = UserInfoForm(instance=profile)
    return render(request, 'update_info.html', {'form': form})
