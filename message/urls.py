from django.urls import path
from .views import MessageMgmt, RecentMessages
urlpatterns = [
    path('recent/', RecentMessages.as_view()),
    path('<str:username>/', MessageMgmt.as_view()),
    path('<str:username>/<str:msgid>/', MessageMgmt.as_view()),
]
