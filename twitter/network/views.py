from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime   
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

from .models import *


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
    #add new post

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)    

    data = json.loads(request.body)    
    
    if 'content' not in data:
            return JsonResponse({"error": "Missing 'content' key in the request data."}, status=400)

    try:        
        post_content = data.get("content").capitalize()
        user = request.user
        post = Posts(created_by= user, content = post_content)
        post.save()
        return JsonResponse({"message": "Post submitted successfully."}, status=201)
    except json.JSONDecodeError as e:
        print(e)  # Log the actual error for debugging purposes
        return JsonResponse({"error": "Post not found."},status=500)

        
@csrf_exempt
@login_required
def all_posts(request,username = None):
    #All posts
    print("Received username:", username) 

    if username:
        user = User.objects.get(username=username)
        print("user in all posts:", user)
        print("username in all posts:", username)
        posts = Posts.objects.filter(created_by = user)


    else:    
        posts = Posts.objects.all()
        print("username in all posts:", username)
        print("running all posts without username:", username)

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    serialized_posts = []

    for post in posts:
        # Retrieve comments and likes associated with the post
        
        likes = Like.objects.filter(post=post)

        # Retrieve comments and likes count
        total_likes = likes.count()

        # Serialize post
        serialized_post_current = post.serialize()

        # Add number of comments and likes to the serialized post data
        serialized_post_current['total_likes'] = total_likes

        user_has_liked =  Like.objects.filter(post=post, liked_by = request.user).exists()
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
        following = user.following.count()
        followers = user.followers.count()

        print("user in profile page:", user)
        print("username in profile page:", username)

    

     # Create a dictionary with user data
        user_data = {
            'username': user.username.capitalize(),
            'email': user.email,
            'following': following,
            'followers': followers,
        }

        return JsonResponse({'user': user_data})
        
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
