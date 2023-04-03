from apps.main.models import Notification

def have_notification(request):
    context = {'have_notification': False}
    if request.user.id:
        user = request.user
        notification = Notification.objects.filter(user_id=user, viewed=False)
    
        if notification.exists():
            context['have_notification'] = True
        
    return context