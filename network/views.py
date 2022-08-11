from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
# paginator
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# posts
def index(request):
    posts_list = Post.objects.all().order_by('-date')
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/index.html", {'posts':posts, 'f':0})


# make a post
@login_required
def makePost(request):
    post = Post(content = request.POST['content'], owner =request.user, likes=0)
    post.save()
    return redirect("/")


# following page
@login_required
def following(request):
    following = Follow.objects.filter(userF=request.user).values_list('owner')
    posts_list = Post.objects.filter(owner__in=following).order_by('-date')
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    print(posts)
    return render(request, "network/index.html", {'posts':posts, 'f':1})

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


# profile
def profile(request, uid):
    puser = User.objects.get(id = uid)
    posts = Post.objects.filter(owner=puser).order_by('-date')
    # follow or unfollow
    follow = 0
    if request.user.is_authenticated: 
        if(request.user.id != puser.id):
            try:
                f = Follow.objects.get(userF=request.user, owner=puser)
                follow = 1
            except Follow.DoesNotExist:
                print("not exist")
        else:
            print("no")

    #  no. of followers
    numOfFollowers = 0
    try:
            f = Follow.objects.filter(owner=puser)
            numOfFollowers = f.count()
    except Follow.DoesNotExist:
        print("not exist")
    # no. of following
    numOfFollowings = 0
    try:
            f = Follow.objects.filter(userF=puser)
            numOfFollowings = f.count()
    except Follow.DoesNotExist:
        print("not exist")

    return render(request, "network/profile.html", {'puser':puser, 'posts':posts, "follow":follow, "numOfFollowers":numOfFollowers, "numOfFollowings": numOfFollowings})

# follow
@login_required
def follow(request, uid):
    puser = User.objects.get(id = uid)
    f = Follow(userF=request.user, owner=puser)
    f.save()
    return redirect("../../profile/"+str(uid))

# unfollow
@login_required
def unfollow(request, uid):
    puser = User.objects.get(id = uid)
    f = Follow.objects.get(userF=request.user, owner=puser)
    f.delete()
    return redirect("../../profile/"+str(uid))

# likes
@login_required
def like(request, pid):
    post = Post.objects.get(id = pid)
    try:
        lik = Like.objects.get(Lowner=request.user, post=post)
        lik.delete()
        post.likes = post.likes - 1
        post.save(update_fields=['likes'])

    except Like.DoesNotExist:
        post.likes = post.likes + 1
        post.save(update_fields=['likes'])
        l = Like(Lowner=request.user, post=post)
        l.save()
            
    return JsonResponse({
            "likes": post.likes
        }, status=400)


# edit
@csrf_exempt
def edit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # get body
    data = json.loads(request.body)
    post = Post.objects.get(id=data.get("pid"))
    post.content = data.get("content")
    post.save(update_fields=['content'])
    return JsonResponse({"message": "1"}, status=400)


