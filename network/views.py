import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

from .models import User, Post, Follow


def index(request):
    if request.method=="GET":
        posts=Post.objects.all().order_by('-date')
        return render(request, "network/index.html", {'posts':posts})
    return render(request, "network/index.html")

def profile_view(request, id):
    user = User.objects.get(pk=id)
    following_count = len(Follow.objects.filter(user_follower=user))
    follower_count = len(Follow.objects.filter(user_following=user))
    is_follower = "Unfollow" if (Follow.objects.filter(user_following=user,
                            user_follower=request.user).exists()) else "Follow"
    return render(request, "network/profile.html", {'user_prof_id':id, 'user_prof':user,
                'following_count':following_count, 'follower_count':follower_count, "is_follower": is_follower})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def new_post(request):
    if request.method == "POST":
        new_post= Post(
            user=User.objects.get(pk=request.user.id),
            content=request.POST["content"]
        )
        new_post.save()
    return HttpResponseRedirect(reverse("index"))

def profile_show(request, profilebox):
    id = int(request.GET.get('id'))
    user = User.objects.get(pk=id)
    if(profilebox == 'post'):
        boxs = Post.objects.filter(user=user)
    if(profilebox == 'following'):
        boxs = Follow.objects.filter(user_follower=user)
    if(profilebox == 'follower'):
        boxs = Follow.objects.filter(user_following=user)
    return JsonResponse([box.serialize() for box in boxs], safe=False)

def follow(request, id):
    user_following = User.objects.get(pk=id)
    is_follower = "Unfollow" if (Follow.objects.filter(user_following=user_following,
                            user_follower=request.user).exists()) else "Follow"
    print(is_follower)
    if is_follower=="Follow":
        new_follow = Follow(
            user_following=user_following, 
            user_follower=request.user
        )
        new_follow.save()
    elif is_follower == "Unfollow":
        cur_following=Follow.objects.get(user_following=user_following, user_follower=request.user)
        cur_following.delete()
    #return HttpResponseRedirect(reverse("profile", kwargs={'id': id}))   
    return JsonResponse({"message": "Follow was set successfully."}, status=201)

    
