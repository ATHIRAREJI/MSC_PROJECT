from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#Models
from feedback.models import Feedback
from feedback.forms import FeedbackForm
from sentimental_analysis import applicationDataPreProcessing
import pickle


# Create your views here.
@login_required
def UserFeedback(request):
    message = ""
    if request.method == "POST":
        #create form instance and populate it with data from the request
        form = FeedbackForm(request.POST)
        # check whether it is valid or not
        if form.is_valid():
            category = form.cleaned_data.get('category')
            feedback= form.cleaned_data.get('feedback')

            #Get sentimental class value of feedback
            x_vector = applicationDataPreProcessing(feedback)
               
            #Load the model
            with open('sentimental-analysis', 'rb') as training_model:
                model = pickle.load(training_model)

            predictions = model.predict(x_vector)

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