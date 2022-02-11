
from django.urls import path
from . import views


urlpatterns = [
    path("",views.home, name="home"),
    path("login",views.login, name="login"),
    path("signin",views.signin, name="signin"),
    path("room/<int:roomid>", views.room, name="room"),
    path("search/<name>",views.search, name="seach"),
    path("searchPage",views.searchPage, name="searchPage"),
    path("profile",views.profile, name="profile"),
    path("logout",views.logoutUser, name="logout"),
    path("searchResult/<username>", views.searchResult, name="searchResult"),
    path("follow/<username>",views.follow, name="follow"),
    path("accept/<username>",views.accept, name="accept"),
    path("decline/<username>",views.decline, name="decline")
]