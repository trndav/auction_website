from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, Comment, Listing, Watchlist, Bid, Category
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import CommentForm

def index(request):
    return render(request, "auctions/index.html")

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
def create_comment(request, listing_id):
    class CommentForm(forms.ModelForm):
        class Meta:
            model = Comment
            fields = ['text']
            labels = {'text': ''}
            widgets = {
                'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'})
            }

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('listing_detail', listing_id=listing_id)
    else:
        form = CommentForm()
    # return render(request, 'auctions/create_comment.html', {'form': form})
    return render(request, 'auctions/listing/listing_detail.html', {'form': form})

def show_comments(request):
    comments = Comment.objects.all()  # Retrieve all comments from the database
    return render(request, 'auctions/show_comments.html', {'comments': comments})

# Show comments on item listing page
def index(request):
    comments = Comment.objects.all()  # Retrieve all comments from the database
    return render(request, 'auctions/listing/listing_detail.html', {'comments': comments})

# Create/load listing model
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'text', 'start_bid', 'image']

# List listing objects
def listing_list(request):
    listings = Listing.objects.all()
    return render(request, 'auctions/listing/index.html', {'listings': listings})

# Create new listing
@login_required(login_url='/login/')
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            category_id = request.POST.get('category') # Retrieve the selected category ID from the form data
            category = Category.objects.get(pk=category_id)  # Retrieve the Category object based on the ID
            
            listing = form.save(commit=False)
            listing.category = category
            listing.user = request.user
            form.save()
            return redirect('listing_list')
    else:
        form = ListingForm()    
    categories = Category.objects.all()    
    return render(request, 'auctions/listing/create_listing.html', {'form': form, 'categories': categories})
    
# Edit listing
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_list')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'auctions/listing/edit_listing.html', {'form': form})

def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        listing.delete()
        return redirect('listing_list')
    return render(request, 'auctions/listing/delete_listing.html', {'listing': listing})

# For single item view listing
@login_required(login_url='/login/')
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    watchlist_items = Watchlist.objects.filter(user=request.user, listing=listing)
    comments = Comment.objects.all()
    comments = listing.comments.all()  # Retrieve comments related to the listing
    category = listing.category
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, listing=listing, text=text)
            return redirect('listing_detail', pk=pk)   
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            # Save the comment to the database
            Comment.objects.create(user=request.user, listing=listing, text=text)
            return redirect('listing_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'auctions/listing/listing_detail.html', {'listing': listing, 'watchlist_items': watchlist_items, 'comments': comments, 'form': form, 'category': category})

# Add to watchlist
@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, listing=listing)
    return redirect('listing_detail', pk=listing_id)

# Remove from watchlist
@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    Watchlist.objects.filter(user=request.user, listing=listing).delete()
    return redirect('listing_detail', pk=listing_id)

# Show watchlist items
def watchlist_page(request):
    listing = Listing.objects.all()
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/listing/watchlist.html', {'watchlist_items': watchlist_items, 'listing': listing})

def place_bid(request, listing_id):
    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        print("Received bid amount:", bid_amount)
        listing = get_object_or_404(Listing, pk=listing_id)

        if float(bid_amount) >= float(listing.start_bid) and float(bid_amount) > float(listing.current_highest_bid):
            listing.current_highest_bid = bid_amount
            listing.start_bid = bid_amount
            print(listing.current_highest_bid)
            listing.save()
            Bid.objects.create(user=request.user, listing=listing, bid_amount=bid_amount)
            return redirect('listing_detail', pk=listing_id)
        else:
            error_message = "Your bid must be large as starting bid and greater than current highest bid."
            return render(request, 'auctions/listing/error.html', {'error_message': error_message})
    else:
        pass

def error(request):
    return render(request, 'error.html')

# Close bid for logged user
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.user:
        listing.is_active = False
        listing.winner = listing.user
        listing.save()
    return redirect('listing_detail', pk=listing_id)

def all_listing(request):
    listings = Listing.objects.all()
    return render(request, 'auctions/listing/all_listing.html', {'listings': listings})

def active_listing(request):
    listings = Listing.objects.all()
    return render(request, 'auctions/listing/active.html', {'listings': listings})

def closed_listing(request):
    listings = Listing.objects.all()
    return render(request, 'auctions/listing/closed.html', {'listings': listings})