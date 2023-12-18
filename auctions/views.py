from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


from .models import User
from .models import Listing
from .models import Bid
from .models import Comment
from .models import Category




    


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


    #create create Listing
def createListing(request):
    if request.method == 'GET':
        allCategories = Category.objects.all()
        return render(request, "auctions/createListing.html", {
            'categories': allCategories
        })
        
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.POST.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_name = request.POST.get('category')
        
        user = request.user
        
        categoryNew = Category.objects.get(categoryName=category_name)


        existing_listing = Listing.objects.filter(title=title, active=True).first()
        
        if existing_listing:
            messages.error(request, 'A listing with the same title already exists.')
            return redirect('createListing')
        
        bid = Bid(bid=int(price))
        bid.save()


        newListing = Listing(
            title=title,
            image=image,
            description=description,
            price=bid.bid,
            category=categoryNew,
            creator=user,
            highestBidder=user,
            active=True 
        )
        newListing.save()

        return redirect('createdPage', title=newListing.title)
                        
def bid(request, title):
    listing = get_object_or_404(Listing, title=title)

    if request.method == 'POST':
        new_bid = int(request.POST.get('bid'))

        if new_bid > listing.price:
            listing.price = new_bid
            listing.highestBidder = request.user #highest bidder
            listing.save()

            return redirect('createdPage', title=listing.title) 
        else:
            messages.error(request, 'The bid must be higher than the price!')
            return render(request, 'auctions/createdPage.html', {
                'listing': listing
                })
            

    return render(request, 'auctions/createdPage.html', {
        'listing': listing
        })

def index(request):
    if request.method == 'GET':
        activeListings = Listing.objects.filter(active=True)
        return render(request, "auctions/index.html", {
            'activeListings': activeListings
        })
    
def winningAuctions(request):
    if request.method == 'GET':
        winning_listings = Listing.objects.filter(active=False, highestBidder=request.user)
        return render(request, "auctions/WinningAuctions.html", {
            'winningAuctions': winning_listings
        })



def createdPage(request, title):
    if request.method == 'GET':
        listing = Listing.objects.get(title=title)
        return render(request, 'auctions/createdPage.html', {
            'listing': listing
        })
    


    
def categories(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        return redirect('category', category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': categories
    })

def category(request, category_id):
    if request.method == 'GET':
        category = get_object_or_404(Category, pk=category_id)
        listings = Listing.objects.filter(category=category)
        return render(request, 'auctions/category.html', {
            'category': category,
            'listings': listings
            })
            
def closeListing(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        if request.user == listing.creator:
            listing.active = False
            listing.save()
        return redirect('index')
     

    
def watchlist(request):
    if request.method == 'GET':
        watchlist_items = request.user.watchlist.filter(active=True)
        return render(request, 'auctions/watchlist.html', {
            'watchlist_items': watchlist_items
            })

    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        listing = get_object_or_404(Listing, pk=listing_id, active=True)
        watchlist_items = request.user.watchlist.all()

        if listing in request.user.watchlist.all():
            request.user.watchlist.remove(listing)
        else:
            request.user.watchlist.add(listing)

        return redirect(request.META.get('HTTP_REFERER', 'index'))
    
def comment(request, title):
    listing = get_object_or_404(Listing, title=title)

    if request.method == 'POST':
        comments = request.POST.get('comments')

        if comments:
            Comment.objects.create(commenter=request.user, listing=listing, comments=comments)

    comments = listing.comment_set.all()

    return redirect('createdPage', title=listing.title)
    