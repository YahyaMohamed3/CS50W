from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect,  get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from .models import User, Posts, Follow
import json
from django.core.paginator import Paginator
from django.http import JsonResponse





class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["content"]


def index(request):
    # Retrieve all posts, ordered by date
    all_posts = Posts.objects.all().order_by("-date")

    # Set up pagination
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": page_obj,
        "page_obj": page_obj,
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


def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('index')
    else:
        form = PostForm()

    return render(request, 'network/post.html', {'form': form})


def profile(request, username):
    # Check if the request method is PUT
    if request.method == "PUT":
        # Load the request body data
        data = json.loads(request.body)
        following = data.get('following')

        current_user = request.user

        user_to_follow = get_object_or_404(User, username=username)

        follow_relation, created = Follow.objects.get_or_create(user=current_user)

        if following:
            follow_relation.following.add(user_to_follow)
        else:
            follow_relation.following.remove(user_to_follow)

        return JsonResponse({"success": True}, status=200)

    # Non-PUT request handling
    profile_user = get_object_or_404(User, username=username)

    # Get the count of followers and following
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    followers = profile_user.followers.all()

    follower_usernames = [follower.user.username for follower in followers]

    posts = Posts.objects.filter(user=profile_user).order_by("-date")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the profile page
    return render(request, "network/profile.html", {
        "user": profile_user,
        "followers_count": followers_count,
        "following_count": following_count,
        "posts": posts,
        "followers": follower_usernames,
        "posts": page_obj,
        "page_obj": page_obj
    })

def following_posts(request):
    user = request.user

    # Ensure the user is authenticated
    if not user.is_authenticated:
        return redirect("index")

    # Get the list of users that the current user is following
    following_users = user.following.values_list('following', flat=True)

    # Check if the user is following anyone
    if not following_users:
        return render(request, "network/index.html", {
            "error_message": "You are currently not following anyone."
        })

    # Retrieve all posts from the users that the current user is following
    posts = Posts.objects.filter(user__id__in=following_users).order_by('-date')

    # Set up pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template with the paginated posts
    return render(request, "network/index.html", {
        "posts": page_obj,
        "page_obj": page_obj,
    })

def toggle_like(request, postId):
    if request.method == "PUT":
        post = Posts.objects.get(id=postId)
        user = request.user
        if not user.is_authenticated:
            return redirect("login")

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return JsonResponse({'success': True, 'liked': liked})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def edit(request , postId):
    if request.method == "PUT":
        user = request.user
        if not user.is_authenticated:
            return redirect("login")
        try:
            post = Posts.objects.get(id=postId)
        except Posts.DoesNotExist:
            return render(request , "network/404.html",{'error_message': 'Post not found'})

        if post.user == user:
            try:
                data = json.loads(request.body)
                content = data.get("content")
                if content:
                    post.content = content
                    post.save()
                    return JsonResponse({'success':'Post updated sucessfully'})
                else:
                    return JsonResponse({'error':'Post content cannot be empty'}, status="400")
            except json.JSONDecodeError:
                return JsonResponse({'error':'Invalid Json data'}, status=400)

        else:
            error_message = "you can only edit posts that you have posted"
            return render(request , "network/404.html", {'error_message': error_message})
    return JsonResponse({'error': 'INvlaid HTTP method'}, status=405)

