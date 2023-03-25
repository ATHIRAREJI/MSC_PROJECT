from django.urls import path
from feedback.views import UserFeedback

urlpatterns = [
    path('', UserFeedback, name='user-feedback'),
]
