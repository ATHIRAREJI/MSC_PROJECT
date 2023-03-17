from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.db.models import Q

from django.contrib.auth.models import User
from message.models import Message

# Create your views here.
@login_required
def UserInbox(request):
    user = request.user
    inbox_messages = Message.get_user_messages(user=user)
    
    active_message = None
    message_data = None

    if inbox_messages:
        first_message = inbox_messages[0]
        active_message = first_message['user'].username
        message_data = Message.objects.filter(user=user, recipient=first_message['user'])
        message_data.update(is_read=True)

        for msg in inbox_messages:
            if msg['user'].username == active_message:
                msg['unread'] = 0


    context = {
        'message_data': message_data,
        'messages': inbox_messages,
        'active_message': active_message,
        'page': 'inbox'
    }

    return render(request, 'message.html',context)


@login_required
def GetDirectMessage(request, username):
    user = request.user
    inbox_messages = Message.get_user_messages(user=user)

    active_message = username
    message_data = Message.objects.filter(user=user, recipient__username = username)
    message_data.update(is_read = True)

    for msg in inbox_messages:
            if msg['user'].username == active_message:
                msg['unread'] = 0

    

    context = {
        'message_data': message_data,
        'messages': inbox_messages,
        'active_message': active_message,
        'page': 'inbox'
    }

    return render(request, 'message.html',context)


@login_required
def SendMessage(request):
     from_user = request.user
     to_username = request.POST.get('to_username')
     message = request.POST.get('message')
     if request.method == 'POST':
        to_user = User.objects.get(username=to_username)  
        Message.create_send_message(from_user, to_user, message)
        return redirect('inbox')
     else:
        HttpResponseBadRequest()

@login_required
def SearchUser(request):
     username = request.user.username
     user_query = request.GET.get('username')
     context = {}

     if user_query:
         users = User.objects.filter(Q(username__icontains=user_query)).exclude(username=username)
         context = {
             'users': users,
             'page': 'inbox'
         }
     else:
         context = {'page': 'inbox'}

     return render(request, 'search_user.html', context)

@login_required
def NewMessage(request, username):
    from_user_info = request.user
    message = 'Says hello!'

    try:
        to_user_info = User.objects.get(username=username)
    except Exception as e:
        return redirect('search-user')
    
    if from_user_info != to_user_info:
        Message.create_send_message(from_user_info, to_user_info, message)

    return redirect('inbox')


