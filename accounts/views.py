from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, SignUpForm
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Log In'})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username,password=password)
        login(request, new_user)
        return redirect('home')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Sign Up'})

def logout_view(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Sign Up'})


