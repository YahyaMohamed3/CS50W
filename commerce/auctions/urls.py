from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("toggle_watchlist/<str:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("place_bid/<str:listing_id>" , views.place_bid, name="place_bid"),
    path("watchlist", views.watchlist , name="user_watchlist"),
    path("close_auction/<str:listing_id>", views.close_auction, name="close_auction"),
    path("add_comment/<str:listing_id>" , views.add_comment , name="add_comment"),
    path("categories" , views.categories , name="categories"),
    path("category_listings/<str:category>" , views.category_listings, name="category_listings"),
]
