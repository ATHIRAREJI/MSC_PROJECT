import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

#Models
from feedback.models import Feedback

# Create your views here.
@login_required
def FeedbackReport(request):
    #Chart labels
    labels = ["positive","negative","neutral"]

    teaching = [0,0,0]
    course_content = [0,0,0]
    examination = [0,0,0]
    labwork = [0,0,0]
    library_facilities = [0,0,0]
    extracurricular_activities = [0,0,0]
    if request.method == "POST":
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        report_data = Feedback.objects.values('category','sentimental_status').filter(date__range=[start_date,end_date]).annotate(sentiments_count=Count('sentimental_status')).values('category','sentimental_status','sentiments_count')
    else:
        today = datetime.datetime.now()
        report_data = Feedback.objects.values('category','sentimental_status').filter(date__month=today.month).annotate(sentiments_count=Count('sentimental_status')).values('category','sentimental_status','sentiments_count')
            
    if report_data:
        for values in report_data:
            category_id = values['category']
            if category_id == 1:
                teaching = createStatusList(teaching,values['sentimental_status'],values['sentiments_count'])
            elif category_id == 2:
                course_content = createStatusList(course_content,values['sentimental_status'],values['sentiments_count'])
            elif category_id == 3:
                examination = createStatusList(examination,values['sentimental_status'],values['sentiments_count'])
            elif category_id == 4:
                labwork = createStatusList(labwork,values['sentimental_status'],values['sentiments_count'])
            elif category_id == 5:
                library_facilities = createStatusList(library_facilities,values['sentimental_status'],values['sentiments_count'])
            else:
                extracurricular_activities = createStatusList(extracurricular_activities,values['sentimental_status'],values['sentiments_count'])
           
    return render(request, 'admin/feedback-report.html', {
        'labels': labels,
        'teaching': teaching,
        'course_content':course_content,
        'examination': examination,
        'labwork': labwork,
        'library_facilities': library_facilities,
        'extracurricular_activities':extracurricular_activities,
        'start_date': '2023-03-28',
        'end_date': '2023-03-28'
    })



def createStatusList(list, status, count):
    if status == 1:
        list[0] = count
    elif status == -1:
         list[1] = count
    else:
         list[2] = count

    return list