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
        labels1 = ["positive","negative"]
        data1 = [45.7, 54.3]
        labels2 = ["veg","no-veg"]
        data2 = [12.7, 87.3]
    else:
        labels1 = ["positive","negative"]
        data1 = [88, 12]

        labels2 = ["veg","no-veg"]
        data2 = [62, 38]


    return render(request, 'admin/feedback-report.html', {
        'labels1': labels1,
        'data1': data1,
        'labels2': labels2,
        'data2': data2,
    })

