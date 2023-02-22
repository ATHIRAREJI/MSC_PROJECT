from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def profile(request):
    return render(request,'profile.html')

def login(request):
    return HttpResponse('hello world')

def signup(request):
    return HttpResponse('hello world')


