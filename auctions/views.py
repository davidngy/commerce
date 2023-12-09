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



def index(request):
    if request.method == 'GET':
        activeListings = Listing.objects.filter(active=True)
        return render(request, "auctions/index.html", {
            'activeListings': activeListings
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
        date = request.POST.get('date')
        price = request.POST.get('price')
        category_name = request.POST.get('category')
         
        categoryNew = Category.objects.get(categoryName = category_name)

        newListing = Listing(
            title=title,
            image=image,
            description=description,
            date=date,
            price=price,
            category=categoryNew,
            active=True 
        )
        newListing.save()

        return redirect('createdPage', title=newListing.title)
                        
def bid(request, title):
    listing = get_object_or_404(Listing, title=title)

    if request.method == 'POST':
        bid = float(request.POST.get('bid'))

        if bid > listing.price:
            listing.price = bid
            listing.save()

            return redirect('createdPage', title=listing.title) 


    return render(request, 'auctions/createdPage.html', {
        'listing': listing})
        

def createdPage(request, title):
    if request.method == 'GET':
        listing = Listing.objects.get(title=title)
        return render(request, 'auctions/createdPage.html', {
            'listing': listing
        })

def watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.user in listing.wathchlist.all():
        listing.wathchlist.remove(request.user)
    else:
        listing.wathchlist.add(request.user)
    
    return redirect('createdPage', title=listing.title)

