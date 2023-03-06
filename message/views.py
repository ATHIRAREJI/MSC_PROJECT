from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
        'active_message': active_message
    }

    return render(request, 'message.html',context)







