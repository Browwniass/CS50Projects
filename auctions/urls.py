from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create_listing", views.create_view, name="create_listing"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist_view, name="watchlist_page"),
    path("new_bid/<int:title>", views.bid_manager, name="bid_page"),
    path("categories", views.categories_view, name="categories"),
    path("my_listing", views.my_listing_view, name="my_listing"),
    path("my_bids", views.my_bids_view, name="my_bids"),
    path("categories/<str:category>", views.find_category, name="find-categories"),
    path("<int:title>", views.page, name="page")
]
