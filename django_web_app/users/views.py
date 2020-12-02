from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login,authenticate
import requests
import json
from blog.models import GithubRespo

def Login(request):
    if request.method=="POST":
        user=authenticate(username=request.POST.get('user'),password=request.POST.get('password'))
        if user:
            login(request,user)
            return redirect('blog-home')
        else:
            return redirect('register')
    return render(request,"users/login.html")




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            for i in form.error_messages.values():
                messages.error(request, i)
    else:
        form = UserRegisterForm()
        print(form)
    return render(request, 'users/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            yoko = requests.get('https://api.github.com/users/%s/repos' %p_form.cleaned_data.get('github'))

            for j in yoko.json():
                print(j['archive_url'],"***",j['name'],"***",j['created_at'],"***",j['contents_url'])
                # k=requests.get('https://api.github.com/users/%s/repos' % p_form.cleaned_data.get('github'))
            #     GithubRespo(profile=request.user.profile,Repso=j)
            p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
