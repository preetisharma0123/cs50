from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime   
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import re

from .models import *
from django.shortcuts import get_object_or_404
from .models import User


def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "network/index.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
@login_required
def new_post(request):
    # add new post
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    if 'content' not in data:
        return JsonResponse({"error": "Missing 'content' key in the request data."}, status=400)

    try:
        post_content = data.get("content").capitalize()
        user = request.user
        post = Posts(created_by=user, content=post_content)
        post.save()

        # Extract and save hashtags
        hashtags = extract_hashtags(post_content)
        for hashtag in hashtags:
            cleaned_hashtag = clean_hashtag(hashtag)
            hashtag_obj, created = Hashtag.objects.get_or_create(name=cleaned_hashtag)
            hashtag_obj.posts.add(post)

        return JsonResponse({"message": "Post submitted successfully."}, status=201)
    except json.JSONDecodeError as e:
        print(e)  # Log the actual error for debugging purposes
        return JsonResponse({"error": "Post not found."}, status=500)

def extract_hashtags(content):
    # Extracts hashtags from the content
    return re.findall(r'#\S+', content)

def clean_hashtag(hashtag):
    # Cleans the hashtag by removing special characters except for hash
    return re.sub(r'[^a-zA-Z0-9#]', '', hashtag).lower()

        
@csrf_exempt
@login_required
def all_posts(request, username=None):
    print("Received username:", username) 

    if username:
        if username != 'following':
            user = User.objects.get(username=username)
            print("user in all posts:", user)
            print("username in all posts:", username)
            posts = Posts.objects.filter(created_by=user)
        else:
            # Get the Following instance for the current user
            following_instance = Following.objects.filter(user=request.user).first()
            if following_instance:
                # Get the users the current user is following
                following_users = following_instance.following.all()
                # Get posts from the users the current user is following
                posts = Posts.objects.filter(created_by__in=following_users)
            else:
                # If the user is not following anyone, return an empty queryset
                posts = Posts.objects.none()
    else:
        posts = Posts.objects.all()
        print("running all posts without username:", username)

    # Return posts in reverse chronological order
    posts = posts.order_by("-timestamp").all()

    serialized_posts = []

    for post in posts:
        # Retrieve comments and likes associated with the post
        likes = Like.objects.filter(post=post)
        comments = Comment.objects.filter(post=post)

        # Retrieve comments and likes count
        total_likes = likes.count()
        total_comments = comments.count()

        # Serialize post
        serialized_post_current = post.serialize()

        # Add number of comments and likes to the serialized post data
        serialized_post_current['total_likes'] = total_likes
        serialized_post_current['total_comments'] = total_comments

        user_has_liked = Like.objects.filter(post=post, liked_by=request.user).exists()
        serialized_post_current['likes'] = user_has_liked

        serialized_posts.append(serialized_post_current)

    # Return serialized data as JSON response
    return JsonResponse({'posts': serialized_posts})



@csrf_exempt
@login_required
def post(request, post_id):
    #TODO
    try:
        post = Posts.objects.get(pk=post_id)
    except Post.doesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    # Post must be via GET 
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)


@csrf_exempt
@login_required
def post_like(request, post_id):
    #post_like

    try:
        post = Posts.objects.get(pk=post_id)

    except Post.doesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Update whether post is liked 
    if request.method == "PUT":
        data = json.loads(request.body)

        # Create a new Like object
        if data.get("likes") is True:
            
            like = Like(post = post, like = True, liked_by = request.user)
            like.save()
            post.save()
            likes = Like.objects.filter(post=post)
            total_likes = likes.count()
            

            # Serialize post
            serialized_post = post.serialize()

            # Add number of  likes to the serialized post data
            serialized_post['total_likes'] = total_likes  
            
            #This will serve to chnage the button text upon clicking        
            serialized_post['likes'] = True
           
            
        else:
            
            # Delete existing Like objects for the post and current user
            Like.objects.filter(post=post, liked_by=request.user).delete()
            post.save()
            try: 
                likes = Like.objects.filter(post=post)
               
                total_likes = likes.count()
                
            except:
                total_likes = 0


            # Serialize post
            serialized_post = post.serialize()

            # Add number of  likes to the serialized post data
            serialized_post['total_likes'] = total_likes

            #This will serve to chnage the button text upon clicking          
        
            serialized_post['likes'] = False
            

        # Return serialized data as JSON response
        return JsonResponse(serialized_post)

    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def post_comments(request, post_id):

    #TODO
    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        # Get pagination parameters from the request
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)

        # Get all comments for the post
        comments = Comment.objects.filter(post=post).order_by('-timestamp')

        # Paginate the comments
        paginator = Paginator(comments, per_page)
        try:
            paginated_comments = paginator.page(page)
        except PageNotAnInteger:
            paginated_comments = paginator.page(1)
        except EmptyPage:
            paginated_comments = paginator.page(paginator.num_pages)

        # Serialize the paginated comments
        comments_data = [comment.serialize() for comment in paginated_comments]

        # Return the paginated comments
        return JsonResponse({
            'comments': comments_data,
            'page': paginated_comments.number,
            'num_pages': paginator.num_pages,
            'total_comments': paginator.count
        })

    # Return post contents
    elif request.method == "PUT":
        data = json.loads(request.body)
        comment = Comment(post=post, text=data['comment'], created_by=request.user)
        comment.save()
        post.save()
        print(comment)
        return JsonResponse(comment.serialize())
    else:
        return JsonResponse({
            "error": "GET/PUT request required."
        }, status=400)


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


@csrf_exempt
@login_required
def profile_page(request,username):
    #Display profile page of the user

    print("Received username:", username) 
    try:
        user = User.objects.get(username=username)
        is_following = None

        # Check if the logged-in user is viewing their own profile
        if user.id != request.user.id:
            # Check if the logged-in user is following the requested profile
            is_following = user in Following.objects.filter(user__id = request.user.id).first().following.all()

        following_count = Following.objects.filter(user__id = user.id).count()  # Number of people this user is following
        followers_count = user.followers.count()  # Number of people following this user

     # Create a dictionary with user data
        user_data = {
            'username': user.username,
            'email': user.email,
            'following': following_count,
            'followers': followers_count,
            'is_following': is_following,
        }

        return JsonResponse(user_data)
        
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


   

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

@csrf_exempt
@login_required
def trending_hashtags(request):
    if request.method != 'GET':
        return JsonResponse({"error": "GET request required."}, status=400)

    hashtags = Hashtag.get_trending_hashtags()
    trending_data = [{"hashtag": hashtag.name, "num_posts": hashtag.num_posts} for hashtag in hashtags]

    return JsonResponse({"trending_hashtags": trending_data}, status=200)

@login_required
def follow_user(request, action, username):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    
    user_to_follow = get_object_or_404(User, username=username)
    current_user = request.user
    
    if action == 'follow':
        if user_to_follow in Following.objects.filter(user__id = request.user.id).first().following.all():
            return JsonResponse({"error": "Already following this user."}, status=400)
        current_user.following.add(user_to_follow)
    elif action == 'unfollow':
        if user_to_follow not in Following.objects.filter(user__id = request.user.id).first().following.all():
            return JsonResponse({"error": "Not following this user."}, status=400)
        current_user.following.remove(user_to_follow)
    else:
        return JsonResponse({"error": "Invalid action."}, status=400)
    
    return JsonResponse({"success": True}, status=200)
