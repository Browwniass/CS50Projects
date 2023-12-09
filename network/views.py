import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import User, Post, Follow, Likes


def index(request):
    if request.method=="GET":
        posts=Post.objects.all().order_by('-date')

        paginator = Paginator(posts, 10)  # Show 10 contacts per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        likes = Likes.objects.all()

        cur_user_liked = []
        try:
            for like in likes:
                if like.user.id == request.user.id:
                    cur_user_liked.append(like.post.id)
        except:
            cur_user_liked = []
        print(cur_user_liked)
        return render(request, "network/index.html", {'posts':posts, 'page_obj':page_obj, 'cur_user_liked': cur_user_liked})
    return render(request, "network/index.html")

def profile_view(request, id):
    user = User.objects.get(pk=id)
    following_count = len(Follow.objects.filter(user_follower=user))
    follower_count = len(Follow.objects.filter(user_following=user))
    is_follower = "Unfollow" if (Follow.objects.filter(user_following=user,
                            user_follower=request.user).exists()) else "Follow"
    
    posts = Post.objects.filter(user=user)
    paginator = Paginator(posts, 1)  # Show 10 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {'user_prof_id':id, 'user_prof':user,
                'following_count':following_count, 'follower_count':follower_count,
                "is_follower": is_follower, 'page_obj':page_obj})

def following_view(request):
    following_list = Follow.objects.filter(user_follower=request.user).values_list("user_following", flat=True)
    following_post = Post.objects.filter(user__id__in=following_list).order_by('-date')
    
    paginator = Paginator(following_post, 1)  # Show 10 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following_page.html", {'posts':following_post, 'page_obj':page_obj})

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
        posts = Post.objects.filter(user=user)

        paginator = Paginator(posts, 1)  # Show 10 contacts per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html", {'posts':posts, 'page_obj':page_obj})

    elif(profilebox == 'following'):
        boxs = Follow.objects.filter(user_follower=user)
    elif(profilebox == 'follower'):
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
    return HttpResponseRedirect(reverse("profile", kwargs={'id': id}))   
    #return JsonResponse({"message": "Follow was set successfully."}, status=201)

    
def saving_edit(request, post_id):
    post=Post.objects.get(id=post_id)
    edit_content = request.GET.get('content')
    if request.user.id == post.user.id:
        post.content = edit_content
        post.save()
    return JsonResponse({"post": f"{edit_content}"}, status=201)

def liking_post(request, post_id):
    post = Post.objects.get(id=post_id)
    is_liked = request.GET.get('is_liked')
    if is_liked == "Like":
        like = Likes(
            post = post,
            user = request.user
        )
        like.save()
    else:
        like = Likes.objects.get(post=post, user=request.user)
        like.delete()
    return JsonResponse({"message": "Like was set successfully."}, status=201)