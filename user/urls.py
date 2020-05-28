from django.urls import path
from .views import UserSignUp, Profile, UserLogin, Logout, UserAutoComplete, SearchInFollowerFollowing
urlpatterns = [
    path('', UserSignUp.as_view()),
    path('me/', Profile.as_view()),
    path('login/', UserLogin.as_view()),
    path('logout/', Logout.as_view()),
    path('auto-complete/', UserAutoComplete.as_view()),
    path('search/', SearchInFollowerFollowing.as_view())
]
