from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import CreateNewUser, EditProfile
from django.contrib.auth import login ,logout, authenticate
from django.urls import reverse , reverse_lazy
from App_Login.models import UserProfile ,Follow
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from App_Posts.forms import PostForm
# Create your views here.

def sing_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render (request,'App_Login/singup.html',context = {'title':'Sing Up', 'form':form})



def login_page(request):
    wrong_password = False
    form = AuthenticationForm()
    if request.method=='POST':
        wrong_password = True
        form = AuthenticationForm(request.POST)
        username = form.request.get('username')
        password = form.request.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            wrong_password = False
            login(request,user)
            return HttpResponseRedirect(reverse('App_Posts:home'))
    return render(request,'App_Login/login.html',context={'title':'Login','form':form,'wrong_password':wrong_password})


@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))


def profile(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('App_Posts:home'))
    return render(request,'App_Login/user.html',context={'form':form,})


@login_required
def edit_Profile(request):
    print(request.user)
    current_user = UserProfile.objects.get(user=request.user)
    
    form = EditProfile(instance=current_user)
    if request.method=='POST':
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))

         
    return render(request,'App_Login/profile.html', context={'title':'Edit Profile','form':form,})




@login_required
def user(request,username):
    user_other = User.objects.get(username=username)
    allready_follow = Follow.objects.filter(follower=request.user,following=user_other)
    if user_other == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request,'App_Login/user_other.html',context={'user_other':user_other,'allready_follow':allready_follow})


@login_required
def follow(request,username):
    following = User.objects.get(username=username)
    follower = request.user
    allready_follow = Follow.objects.filter(follower=follower, following=following)
    if not allready_follow:
        followed_user = Follow(following=following,follower=follower)
        followed_user.save()
    return HttpResponseRedirect(reverse('App_Login:user', kwargs={'username':username}))


@login_required
def unfollow(request,username):
    following = User.objects.get(username=username)
    follower = request.user
    allready_follow = Follow.objects.filter(follower=follower,following=following)
    allready_follow.delete()
    return HttpResponseRedirect(reverse('App_Login:user', kwargs={'username':username}))