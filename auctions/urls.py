from django.urls import path
from .views import bid

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.createListing, name="createListing"),
    path('bid/<str:title>/', views.bid, name='bid'),
    path("createdPage/<str:title>/", views.createdPage, name="createdPage"),
    path("watchlist", views.watchlist, name="watchlist")
]
