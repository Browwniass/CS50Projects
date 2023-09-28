from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms 

from .models import User, Listings, Bids, Categories
 

class NewListingForm(forms.Form):
    title = forms.CharField(max_length=100, label="",
                            widget= forms.TextInput
                            (attrs={'class':'form-control', 
                            'placeholder': 'Title'}))
    bid = forms.IntegerField(min_value=0, label="",
                           widget= forms.NumberInput
                           (attrs={'class':'form-control',
                            'placeholder': 'Bid'}))
    description = forms.CharField(max_length=400, label="",
                           widget= forms.Textarea
                           (attrs={'class':'form-control',
                            'placeholder': 'Description'}))
    photo = forms.CharField(max_length=60, label="",
                           widget= forms.URLInput
                           (attrs={'class':'form-control',
                            'placeholder': 'Photo URL'}), required=False)
    categories = forms.ChoiceField(choices=[
                            (choice.pk, choice.title) for choice in Categories.objects.all()],
                            required=False , label="",
                           widget= forms.Select
                           (attrs={'class':'form-control',
                            'placeholder': 'Category[Optional]'})) 
    
    """forms.CharField(max_length=60, label="",
                           widget= forms.TextInput
                           (attrs={'class':'form-control',
                            'placeholder': 'Category'}))"""

def index(request):
    forms = Bids.objects.filter(listing__is_active=True).select_related('listing')
    return render(request, "auctions/index.html", {'forms':forms})


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
                id_categories=Categories.objects.get(pk=form.cleaned_data['categories'])
            )
            listing.save()
            bid = Bids(
                author=request.user, 
                listing=listing,
                price=form.cleaned_data['bid']
            )
            bid.save()


    return render(request, "auctions/create_listing.html", 
        {"form":NewListingForm()})

