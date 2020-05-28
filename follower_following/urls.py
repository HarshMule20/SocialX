from django.urls import path
from .views import Following, FollowerFollowing, Unfollow

urlpatterns = [
    path('following/', Following.as_view()),
    path('dashboard/', FollowerFollowing.as_view()),
    path('unfollow/', Unfollow.as_view())
]