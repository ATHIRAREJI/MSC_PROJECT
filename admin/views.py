from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

#Models
from user_auth.models import Profile
from post.models import Post, Follow, Stream

# Create your views here.
@login_required
def FeedbackReport(request):
    if request.method == "POST":
        labels = ["positive","negative"]
        data = [45.7, 54.3]
    else:
        labels = ["positive","negative"]
        data = [88, 12]

    return render(request, 'admin/feedback-report.html', {
        'labels': labels,
        'data': data,
    })

