from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from django.contrib.auth.decorators import login_required

from .models import *
from django.shortcuts import redirect

import datetime


# Forms

class NewListingForm(forms.Form):
    """
        Form to add a new listing
    """
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    startBid = forms.FloatField()
    imgUrl = forms.URLField(required=False)
    category = forms.CharField(max_length=100, required=False)

class NewBidForm(forms.Form):
    value = forms.FloatField()

class NewCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    items = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        'items': items
    })

def login_view(request):
    if request.method == "POST":
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
def createListing(request):
    if request.method == 'GET':

        form = NewListingForm()
        return render(request, 'auctions/createListing.html',{
            'form': form
        })

    else:
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data['description']
            startBid = form.cleaned_data['startBid']
            imgUrl = form.cleaned_data['imgUrl']
            category = form.cleaned_data['category']
            newListing = AuctionListing(owner=request.user, title=title,description=description, currentBid=startBid, imgUrl=imgUrl, category=category, active=True)
            newListing.save()
        return redirect('index')

def viewListing(request, pk):
    if request.method == 'GET':
        item = AuctionListing.objects.get(id=pk)
        comments = Comment.objects.filter(item=item.id)
        bids = Bid.objects.filter(item=item.id)
        sameUser = str(item.owner.username) == str(request.user.username)
        bidForm = NewBidForm(initial={'value': item.currentBid})
        try:
            watchlistItem = Watchlist.objects.get(item=pk)
        except: 
            watchlistItem = None

        return render(request, 'auctions/viewListing.html', {
            'item': item,
            'sameUser': sameUser,
            'commentForm': NewCommentForm(),
            'bidForm': bidForm,
            'comments': comments,
            'watchlistItem': watchlistItem,
            'userLoged': request.user.username,
        })
    else:
        form = NewCommentForm(request.POST)
        formTwo = NewBidForm(request.POST)
        if form.is_valid() and form:
            content = form.cleaned_data["content"]
            item = AuctionListing.objects.get(id=pk)
            date = datetime.datetime.now()
            newComment = Comment(item=item, name=request.user, content=content, date=date)
            newComment.save()    
        if formTwo.is_valid() and formTwo:
            user = request.user
            item = AuctionListing.objects.get(id=pk)
            value = formTwo.cleaned_data["value"]
            if value <= item.currentBid:
                comments = Comment.objects.filter(item=item.id)
                bids = Bid.objects.filter(item=item.id)
                sameUser = str(item.owner) == str(request.user)
                try:
                    watchlistItem = Watchlist.objects.get(item=pk)
                except: 
                    watchlistItem = None
                bidForm = NewBidForm(initial={'value': item.currentBid})
                return render(request, 'auctions/viewListing.html', {
                    'item': item,
                    'sameUser': sameUser,
                    'commentForm': NewCommentForm(),
                    'bidForm': bidForm,
                    'comments': comments,
                    'userLoged': request.user.username,
                    'watchlistItem': watchlistItem,
                    'message': "Bid too low",
                })
            else:
                item.currentBid = value
                bid = Bid(item=item, name=user, value=value)
                item.save()
                bid.save()
        return redirect('view-listing', item.id)


@login_required
def watchlist(request, pk):
    myItem = AuctionListing.objects.get(id=pk)
    user = request.user

    try:
        itemWatchlist = Watchlist.objects.get(item=myItem, name=user)
    except:
        itemWatchlist = None

    if itemWatchlist:
        itemWatchlist.delete()
    else: 
        itemWatchlist = Watchlist(item = myItem, name=user, idNumber=pk)
        itemWatchlist.save()

    return redirect('view-listing', pk)

@login_required
def myWatchlist(request):
    user = request.user
    try:
        watchlistItems = Watchlist.objects.filter(name=user)
    except:
        watchlistItems = None
    return render(request, 'auctions/watchlist.html', {
        'watchListItems': watchlistItems,
    })


def categories(request):
    items = AuctionListing.objects.order_by('category').values('category').distinct()

    return render(request, 'auctions/categories.html', {
        'items': items
    })


def category(request, categ):
    items = AuctionListing.objects.filter(category=categ)

    return render(request, 'auctions/index.html', {
        'items': items
    })


def closeItem(request, pk):
    item = AuctionListing.objects.get(id=pk)
    item.active = False
    bid = Bid.objects.filter(item=item).latest('value')
    item.winner = bid.name.username
    item.save()


    return redirect('index')