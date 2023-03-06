from django.urls import path
from message.views import UserInbox

urlpatterns = [
    path('', UserInbox, name='inbox'),
]