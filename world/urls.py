from django.urls import path
from .views import Login , Register , MyProfile ,ShopView ,SendBottle , GetBottle ,BottleInbox , BottleSent , ResponseToBottle ,LeaderBoard

urlpatterns = [
    path('login/',Login.as_view()),
    path('register/',Register.as_view()),
    path('profile/',MyProfile.as_view()),
    path('shop/',ShopView.as_view()),
    path('send/',SendBottle.as_view()),
    path('get/',GetBottle.as_view()),
    path('inbox/',BottleInbox.as_view()),
    path('sent/',BottleSent.as_view()),
    path('responce/',ResponseToBottle.as_view()),
    path('leaderboard/',LeaderBoard.as_view()),
]