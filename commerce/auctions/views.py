from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import ListingForm
from .models import User, Listing , Bid , Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings" : listings})


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

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('index')
        else:
            # Display form errors in template
            return render(request, 'auctions/create_listing.html', {
                'form': form,
                'errors': form.errors  # Passing errors to the template
            })
    else:
        form = ListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})

@login_required
def listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    # Get the highest bid for the listing, if it exists
    highest_bid = listing.bids.order_by('-bid_amount').first()

    comments = listing.comments.all()

    # Determine the current bid amount and highest bidder
    if highest_bid:
        current_bid = highest_bid.bid_amount
        highest_bid_user = highest_bid.user
    else:
        current_bid = listing.starting_bid
        highest_bid_user = None  # if No bids are placed

    # Check if the current user is the highest bidder
    user_is_highest_bidder = highest_bid_user == request.user if highest_bid_user else False

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'current_bid': current_bid,
        'highest_bid_user': highest_bid_user,
        'user_is_highest_bidder': user_is_highest_bidder,
        'comments': comments,
    })

@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    # Check if the listing is already in the user's watchlist
    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)

    # Redirect to the listing page
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))


@login_required
def place_bid(request , listing_id):
    listing = get_object_or_404(Listing, id = listing_id)
    if request.method == "POST":
        bid_amount = int(request.POST["bid_amount"])
        highest_bid = listing.bids.order_by("-bid_amount").first()
        current_bid = highest_bid.bid_amount if highest_bid else listing.starting_bid

        if bid_amount < listing.starting_bid or (highest_bid and bid_amount <= highest_bid.bid_amount):
            return render(request , "auctions/listing.html", {"listing": listing,"current_bid":current_bid,
                "error": "Bid must be higher than the current highest bid and starting bid."})
        Bid.objects.create(listing=listing, user=request.user, bid_amount=bid_amount)

        return HttpResponseRedirect(reverse("listing" , kwargs={"listing_id":listing_id}))
    return HttpResponseRedirect(reverse("listing" , kwargs={"listing_id":listing_id}))



@login_required
def watchlist(request):
    watchlist_items = request.user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {'watchlist_items': watchlist_items})


@login_required
def close_auction(request , listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing , pk=listing_id)
        if request.user != listing.user:
            return HttpResponseRedirect(reverse("listing" , kwargs={"listing_id":listing_id}))

        listing.is_active = False
        listing.save()

        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id":listing_id}))

@login_required
def add_comment(request ,listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing , pk=listing_id)
        comment_text = request.POST.get("comment", "").strip()
        if comment_text:
            Comment.objects.create(
                listing = listing,
                user = request.user,
                text = comment_text,
            )
            return HttpResponseRedirect(reverse("listing" , kwargs={"listing_id":listing_id}))
        else:
            messages.error(request, "Comment cannot be empty.")

        # Redirecting back to the listing page
        return redirect('listing', listing_id=listing_id)


@login_required
def categories(request):
    category_choices = [choice[0] for choice in Listing.CATEGORY_CHOICES]
    return render(request , "auctions/categories.html" , {"categories":category_choices})


@login_required
def category_listings(request , category):
    if category:
        listings = Listing.objects.filter(category=category, is_active=True)  # Filter listings by category
        return render(request , "auctions/category_listing.html", {"listings":listings})




