from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#Models
from feedback.models import Feedback
from feedback.forms import FeedbackForm
from test import test


# Create your views here.
@login_required
def UserFeedback(request):
    message = test()
    if request.method == "POST":
        #create form instance and populate it with data from the request
        form = FeedbackForm(request.POST)
        # check whether it is valid or not
        if form.is_valid():
            category = form.cleaned_data.get('category')
            feedback= form.cleaned_data.get('feedback')
            user_id = request.user.id
            sentimental_status = 1
            feedback_obj = Feedback(user_id=user_id,category=category,feedback=feedback,sentimental_status=sentimental_status)
            feedback_obj.save()
            message  =  "success"

    else:
        form = FeedbackForm()

    context = {
        'form': form,
        'message': message
    }
    return render(request,'feedback.html', context)