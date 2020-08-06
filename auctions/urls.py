from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.createListing, name="create-listing"),
    path('view-listing/<str:pk>', views.viewListing, name='view-listing'),
    path('watchlist/<str:pk>', views.watchlist, name='watchlist'),
    path('my-watchlist', views.myWatchlist, name='my-watchlist'),
    path('categories', views.categories, name='categories'),
    path('category/<str:categ>', views.category, name='category'),
    path('close/<str:pk>', views.closeItem, name='close-item'),

]   


