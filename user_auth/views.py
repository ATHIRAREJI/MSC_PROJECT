from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from .forms import SignupForm, ChangePasswordForm, ProfileEditForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.db import transaction

from user_auth.models import Profile
from post.models import Post, Follow, Stream

# Create your views here.
def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    print(profile)
    posts = Post.objects.filter(user=user).order_by('-posted_date')

    #Profile counts
    post_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()

    #Check logged in user follow this profile
    follow_or_not  = Follow.objects.filter(follower=request.user, following=user).exists()

    template = loader.get_template('profile.html')
    context = {
        'posts': posts,
        'profile': profile,
        'post_count': post_count,
        'following_count': following_count,
        'follower_count': followers_count,
        'follow_or_not': follow_or_not
    }
    return HttpResponse(template.render(context, request))

def Signup(request):
    if request.method == "POST":
        #create form instance and populate it with data from the request
        form = SignupForm(request.POST)
        # check whether it is valid or not
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username= form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            User.objects.create_user(username=username,email=email,password=password)
            return redirect('editprofile')
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    
    return render(request,'signup.html', context)

@login_required
def PasswordChange(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change_password_done')
        
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form': form
    }

    return render(request, 'change_password.html',context)


def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')


@login_required
def ProfileFollow(request, username, option):
    user = request.user
    following_user = get_object_or_404(User, username= username)
    
    try:
        f, created = Follow.objects.get_or_create(follower=user, following= following_user)
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following_user, user = user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following_user)[:10]
            with transaction.atomic():
                for post in posts:
                    stream =  Stream(post=post, user=user, date=post.posted_date, following = following_user)
                    stream.save()
        
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))

@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.profile_picture = form.cleaned_data.get('profile_picture')
            profile.course = form.cleaned_data.get('course')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('index')
    else:
        form = ProfileEditForm()

    context = {
        'form': form
    }


    return render(request, 'profile_edit.html', context)

    



