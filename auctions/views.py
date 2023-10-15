from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse 
from django.contrib import messages
from django.db.models import Q

from .forms import NewListingForm, NewBidForm
from .models import User, Listings, Bids, Categories, Comments, Watchlist
 
def index(request):
    forms = Bids.objects.filter(listing__is_active=True, is_current=True).select_related('listing')

    return render(request, "auctions/index.html", {'forms':forms})

def watchlist_view(request):
    watchs=(Watchlist.objects.filter(author=request.user, listing__is_active=True)).values_list('listing', flat=True)
    form = Bids.objects.filter(listing__in=watchs, is_current=True).select_related('listing')
    return render(request, "auctions/watchlist_page.html", {'forms':form})

def categories_view(request):
    categories=Categories.objects.all()
    return render(request, "auctions/categories.html", {'categories':categories})

def my_bids_view(request):
    forms = Bids.objects.filter(author=request.user).select_related('listing')
    return render(request, "auctions/my_bids.html", {'forms':forms})

def my_listing_view(request):
    forms = Bids.objects.filter(listing__author=request.user, is_current=True).select_related('listing')
    return render(request, "auctions/my_listing.html", {'forms':forms})

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


def create_view(request):   

    if request.method=="POST":
        
        form = NewListingForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data['categories'])
            listing = Listings(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                photo=form.cleaned_data['photo'],
                author=request.user, 
                is_active=True,
                id_categories=Categories.objects.get(pk=form.cleaned_data['categories']),

            )
            listing.save()
            bid = Bids(
                author=request.user, 
                listing=listing,
                price=form.cleaned_data['bid'],
                is_current=True
            )
            bid.save()
            
            return HttpResponseRedirect(reverse("page", kwargs={'title': listing.pk}))
        else:
            return render(request, "auctions/create_listing.html", {
                "message": "Invalid Data", "form":form
            })

    return render(request, "auctions/create_listing.html", 
        {"form":NewListingForm()})

def new_bid(request, title):
    form = NewBidForm(request.POST)                       
    if form.is_valid() and not(type(form.cleaned_data['bid']) is type(None)):
        listing=Listings.objects.get(pk=title) 
        bid=Bids.objects.get(listing=listing, is_current=True)
        if bid.price < form.cleaned_data['bid']:
            bid.is_current=False
            bid.save()
            new_bid = Bids(
                author=request.user, 
                listing=listing,
                price=form.cleaned_data['bid'],
                is_current=True
            )
            new_bid.save()
            
            messages.success(request, 'Your bid has been successfully added')
            return HttpResponseRedirect(reverse("page", kwargs={'title': title}))
        else:                
            messages.error(request, 'Your bid must be greater than current')
            return HttpResponseRedirect(reverse("page", kwargs={'title': title}))
    else:
        messages.error(request, 'Invalid input')
        return HttpResponseRedirect(reverse("page", kwargs={'title': title})) 

def close_listing(request, title):
    listing=Listings.objects.get(pk=title)
    bids=Bids.objects.get(listing=listing, is_current=True)

    listing.is_active=False
    listing.owner=bids.author

    listing.save()
    messages.success(request, 'Your successufly close listing')
    return HttpResponseRedirect(reverse("page", kwargs={'title': title}))

def adding_watchlist(request, title, page_redirect):
    listing=Listings.objects.get(pk=title)
    watchlist_search=(Watchlist.objects.filter(author=request.user, listing=listing)).count()
    if watchlist_search==0:
        watchlist = Watchlist(
            author=request.user, 
            listing=listing
        )
        watchlist.save()
    print(page_redirect)
    if page_redirect=="page":
        return HttpResponseRedirect(reverse(f"{page_redirect}", kwargs={'title': title}))   
    return HttpResponseRedirect(reverse(f"{page_redirect}"))

def remove_watchlist(request, title):
    listing=Listings.objects.get(pk=title)
    watchlist_search=Watchlist.objects.get(author=request.user, listing=listing)
    watchlist_search.delete()
    return HttpResponseRedirect(reverse("watchlist_page"))

def post_comment(request, title):
    listing=Listings.objects.get(pk=title)
    comment = request.POST["comment"]
    new_comment= Comments(
        author=request.user, 
        comment=comment,
        listing=listing,
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("page", kwargs={'title': title}))   



def bid_manager(request, title):
    if request.POST.get("but-sub"):
        return new_bid(request, title)
    elif request.POST.get("but-close"):
        return close_listing(request, title)
    elif request.POST.get("but-watchlist"):
        page_redirect=request.POST.get("redirect-form")
        return adding_watchlist(request, title, page_redirect)
    elif request.POST.get("but_rem_watch"):
        return remove_watchlist(request, title)
    elif request.POST.get("but_comment"):
        return post_comment(request, title)

    
def page(request, title):
    listing=Listings.objects.get(pk=title)
    if listing:       
        comments=Comments.objects.filter(listing=listing)
        bids=Bids.objects.filter(listing=listing).values()
        bid=bids.get(is_current=True)
        bid_author=User.objects.get(pk=bid.get("author_id"))
        return render(request, "auctions/page.html", {
            "title": title, "listing": listing, "comments": comments, "bid_author": bid_author, "bid": bid.get("price"),
            "bid_form": NewBidForm()})
    else:
        return render(request, "auctions/error.html")
    
def find_category(request, category):
    category=Categories.objects.get(title=category)
    forms = Bids.objects.filter(listing__is_active=True, listing__id_categories=category, is_current=True).select_related('listing')

    return render(request, "auctions/category_page.html", {'category':category,'forms':forms})