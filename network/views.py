from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request):

    p = Paginator(Post.objects.all().order_by("-timestamp"), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)


    if request.user in User.objects.all():
        if not Follower.objects.filter(user = request.user):
            follower = Follower(user=request.user)
            follower.save()
            print("ok this is gonna work")
        current_user = request.user
        liked_posts = current_user.posts.all()

    else:
        liked_posts = None


    return render(request, "network/index.html", {
        "posts": posts,
        "liked_posts": liked_posts
    })


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

@login_required(login_url="login")
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
        follower = Follower(user=request.user)
        follower.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url="login")
def create(request):
    if request.method == "GET":
        return render(request, "network/create.html")
    elif request.method == "POST":
        content = request.POST["content"].strip()
        if content == "":
            return render(request, "network/create.html", {
                "message": "Cannot make an empty quack!"
            })
        creator = request.user

        post = Post(
            likes=0,
            creator=creator,
            content=content
        )
        post.save()

        return HttpResponseRedirect(reverse("index"))

def user(request, num):

    profile = User.objects.get(user_id = num)
    posts = Post.objects.filter(creator=profile)
    follower_profile = Follower.objects.get(user=profile)
    following_count = follower_profile.following_list.all().count()
    follower_count = Follower.objects.filter(following_list=profile).all().count()

    p = Paginator(posts.order_by("-timestamp"), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    current_user = request.user
    if current_user in User.objects.all():
        liked_posts = current_user.posts.all()
        current_following = Follower.objects.get(user=current_user).following_list.all()
        if profile in current_following:
            is_following = True
        else:
            is_following = False
    else:
        is_following = False
        liked_posts = None

    return render(request, "network/index.html", {
        "posts":posts,
        "profile":profile,
        "follower_count": follower_count,
        "following_count":following_count,
        "is_following":is_following,
        "liked_posts": liked_posts
    })

@login_required(login_url="login")
def following(request):

    current_user = request.user
    liked_posts = current_user.posts.all()
    current_user_following = Follower.objects.get(user=current_user).following_list.all()
    posts = Post.objects.none()

    for user in current_user_following:
        posts |= Post.objects.filter(creator=user)
    
    
    p = Paginator(posts.order_by("-timestamp"), 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    return render(request, "network/index.html", {
        "following": True,
        "posts": posts,
        "liked_posts":liked_posts

    })

def update_followers(request, num):
    current_user = request.user
    other_user = User.objects.get(user_id=num)
    current_user_object = Follower.objects.get(user=current_user)
    if other_user not in current_user_object.following_list.all():
        current_user_object.following_list.add(other_user)
    else:
        current_user_object.following_list.remove(other_user)

    current_user_object.save()

    count = Follower.objects.filter(following_list=other_user).all().count()

    return JsonResponse({"count": count}, status=201)


def like_update(request, num):

    current_post = Post.objects.get(post_id=num)
    current_user = request.user
    current_user_liked_posts = current_user.posts.all()
    if current_post in current_user_liked_posts:
        current_post.likes -= 1
        current_post.save()
        current_user.posts.remove(current_post)
        new_action = "like"
    else:
        current_post.likes += 1
        current_post.save()
        current_user.posts.add(current_post)
        new_action = "unlike"

    current_post.save()
    current_user.save()
    count = current_post.likes

    return JsonResponse({"count": count, "new_action":new_action}, status=201)


def edit_post(request, num, text):
    current_post = Post.objects.get(post_id=num)
    current_post.content = text
    current_post.save()
    return JsonResponse({"alert":"post edited correctly"}, status=201)