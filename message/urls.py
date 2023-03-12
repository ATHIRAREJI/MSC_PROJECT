from django.urls import path
from message.views import UserInbox,GetDirectMessage,SendMessage,SearchUser,NewMessage

urlpatterns = [
    path('', UserInbox, name='inbox'),
    path('dm/<username>', GetDirectMessage, name="dm"),
    path('send',SendMessage, name="send"),
    path('search',SearchUser, name="search-user"),
    path('message/<username>',NewMessage,name="newmessage")
]