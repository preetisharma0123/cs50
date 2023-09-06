from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.commodities, name="commodities"),
    path("create", views.create_listing, name="create"),
    path("search/",views.search, name = "search"),
    path("listing/<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("addWatchlist/<int:listing_id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:listing_id>", views.removeWatchlist, name="removeWatchlist"),
    path("listing/<int:listing_id>/bid", views.addBid, name="addBid"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("watchlist", views.user_watchlist, name="watchlist"),
]
