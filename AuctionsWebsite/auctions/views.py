from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
import datetime

from .models import *


def index(request):
    activeListings = Auction_listing.objects.filter(isActive = True).order_by('-date')
    categories = Category.objects.all()


    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": categories
            })

def listing(request,listing_id):
    try:

        auction = Auction_listing.objects.get(pk =listing_id)
        watchlisted = request.user in auction.watchlist.all()
        comments = Comment.objects.filter(auction_listing = auction)
        bid_count = auction.bids.count()

        if not bid_count :
            bid_value = auction.starting_value
            
        else:


            max_bid = Bid.objects.filter(auction_listing=listing_id).order_by('-bid_value').first()
            bid_value = max_bid.bid_value
            winner = max_bid.created_by.username.capitalize()

            winner_email = max_bid.created_by
            owner = auction.created_by.username.capitalize()
            owner_email = auction.created_by
            

        if auction.isActive:
            return render(request, "auctions/listing.html", {
                "auction": auction,
                "bid_count": f" {bid_count} bid(s) so far. Please make sure that your bid value is greater than ${bid_value}.",
                "comments":comments,
                "bid_value": bid_value, 
                "watchlisted":watchlisted           
                })
       
        elif (request.user == max_bid.created_by and not auction.isActive):

            return render(request, "auctions/closed.html",{
            "message": F"Congratulation!!! You won the auction by ${bid_value}. You can contact the auction owner - {owner} at {owner_email}."
            })

        else:
            print("max bid value in lisiting: closed",bid_value)
            return render(request, "auctions/closed.html",{
                "message": f"listing no longer active. Bid is won by ${bid_value} by user- {winner}.",
                })


    except Exception:
        import traceback
        print(traceback.format_exc())
        return render(request, "auctions/error.html",{
            "message": "Listing does not exists!"
            })   

def categories(request):
    
    cat_all = Category.objects.all()

    return render(request,"Auctions/categories.html",{
        "cat_all" : cat_all
         })
        
def commodities(request,category_id):

    category = Category.objects.get(pk =category_id)
    activeListings = Auction_listing.objects.filter(isActive = True, category = category)
    categories = Category.objects.all()

    return render(request,"Auctions/commodities.html",{
        "listings": activeListings,
        "category": category,
        "categories": categories

         })

def comment(request, listing_id):
    auction = Auction_listing.objects.get(pk =listing_id)
    if request.method =="POST":
            if request.user.is_authenticated:
                recent_comment = request.POST['comment']
                Comment(comment = recent_comment, auction_listing = auction,created_by = request.user).save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                return HttpResponseRedirect(reverse("login"))

def addBid(request, listing_id):

    if request.method =="POST":

        auction = Auction_listing.objects.get(pk =listing_id)
        watchlisted = request.user in auction.watchlist.all()
        comments = auction.comments.all()
        bid_count = auction.bids.count() 

        if not bid_count :
            bid_value = auction.starting_value

        else: 
            # implement code for max bid value
            bid = auction.bids.aggregate(Max('bid_value'))
            bid_value = int(bid["bid_value__max"])
                

        if request.user.is_authenticated and request.POST['bid']:
            bid_submitted = int(request.POST['bid'])
            if bid_submitted > bid_value :
                latest_bid = Bid(auction_listing = auction,bid_value=bid_submitted, created_by = request.user)
                latest_bid.save()
                bid_count = auction.bids.count()
                bid_value = latest_bid.bid_value

                return render(request, "auctions/listing.html", {
                        "auction": auction,
                        "message": "Bid submission successful!",
                        "bid_count": f"{bid_count} bid(s) so far. Please make sure that your bid value is greater than ${bid_value}.",
                        "comments":comments,
                        "bid_value" : bid_value,
                        "watchlisted":watchlisted 
                })

            else:

                return render(request, "auctions/error.html", {
                "message": f"Please make sure your bid value is greater than ${bid_value} ", 
                })
                       
        else:
            return render(request, "auctions/login.html")


def close_listing(request, listing_id):
    # Get current auction if exists
    try:
        auction = Auction_listing.objects.get(pk =listing_id)
        bid_count = auction.bids.count()
        if not bid_count :
            bid_value = auction.starting_value
            
        else:

            max_bid = Bid.objects.filter(auction_listing=listing_id).order_by('-bid_value').first()
            bid_value = max_bid.bid_value
            won_by = max_bid.created_by.username.capitalize()
            winner_email = max_bid.created_by

    except Auction.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Auction id doesn't exist"
        })


    if request.method == "POST":
        if request.user.is_authenticated and request.user.email == auction.created_by.email:
            auction.isActive = False
            auction.save()
            return render(request, "auctions/closed.html",{
                "message": f"listing closed successfully!. Bid has won by ${bid_value} by user - {won_by}. Please contact user at email: {winner_email}"
            })
                
        else:
            return render(request, "auctions/error.html",{
                "message": "Make sure you are the owner of the Listing, you are trying to close."
            })

def removeWatchlist(request,listing_id):
    auction = Auction_listing.objects.get(pk =listing_id)
    auction.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing",args=(listing_id,)))

def addWatchlist(request,listing_id):
    auction = Auction_listing.objects.get(pk =listing_id)
    auction.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def user_watchlist(request):
# Takes User model and it's watchlist object

    listings = request.user.listingwatchlist.all()       
    if request.method =="GET":
        return render(request, "auctions/watchlist.html", {
            "listings": listings
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



     
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        auctions = Auction_listing.objects.filter(title__icontains = entry_search)
        if auctions:
            return render(request, "auctions/search.html",{
                "listings" : auctions
            })           
        else:
            return render(request, "auctions/error.html",{
                "message": "No listings available with this name!"
            })


def create_listing(request):
    
     if request.user.is_authenticated:
        
        if request.method == "GET":
            categories = Category.objects.all()
            return render(request,"Auctions/create.html",{
                "categories" : categories
                })
        else:
            # Get the data from the form

            title = request.POST['title']
            content = request.POST['content']
            image = request.POST['image']
            starting_value = request.POST['starting_value']
            created_by = request.user
            date = datetime.date.today()
            isActive = True

            #get the category
            category = Category.objects.get(cat_name = request.POST['category'])

            # Create new listing
            a1 = Auction_listing(title = title,content = content,starting_value = starting_value ,category = category,created_by = created_by, date = date,isActive = isActive , image = image)
            
            a1.save()
            bid_count = 0
            bid_value = starting_value

            return render(request,"Auctions/listing.html",{
                    "auction": a1,
                    "bid_count": f" {bid_count} bid(s) so far. Please make sure that your bid value is greater than ${bid_value}.",
                    "bid_value":bid_value, 
                    "watchlisted":False
                })
              
     else:
        return HttpResponseRedirect(reverse("login"))
