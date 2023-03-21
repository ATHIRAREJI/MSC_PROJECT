from django.urls import path
from admin.views import FeedbackReport

urlpatterns = [
    path('', FeedbackReport, name='feedback-report'),
]
