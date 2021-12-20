
from django.urls import path
from . import views


urlpatterns = [
    path("",views.home, name="home"),
    path("login",views.login, name="login"),
    path("signin",views.signin, name="signin"),
    path("room/<int:roomid>", views.room, name="room"),
    path("search/<name>",views.search, name="seach")
]