from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.listing_list, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('auctions/listing/create-comment/', views.create_comment, name='create_comment'),
    path('auctions/listing/show-comments/', views.show_comments, name='show_comments'),
    path("auctions/listing/create_listing/", views.create_listing, name="create_listing"),
    path("auctions/listing/edit_listing/", views.edit_listing, name="edit_listing"),
    path("auctions/listing/<int:pk>/delete/", views.delete_listing, name="delete_listing"),
    path("auctions/listing/listing_list/", views.listing_list, name="listing_list"), 
    path("auctions/listing/<int:pk>/", views.listing_detail, name="listing_detail"), 
    path('auctions/listing/add_to_watchlist/<int:listing_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('auctions/listing/remove_from_watchlist/<int:listing_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('auctions/listing/watchlist/', views.watchlist_page, name='watchlist_page'),
    path('auctions/listing/<int:listing_id>/place_bid/', views.place_bid, name='place_bid'),
    path('auctions/listing/error/', views.error, name='error'),
    path('auctions/listing/<int:listing_id>/close/', views.close_auction, name='close_auction'),
    path('auctions/listing/all_listing/', views.all_listing, name='all_listing'),

    path('auctions/listing/active_listing/', views.active_listing, name='active_listing'),
    path('auctions/listing/closed_listing/', views.closed_listing, name='closed_listing'),
    # Images do not display without this:
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
