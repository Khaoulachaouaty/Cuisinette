def notification_context(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.all().order_by('-created_at')  
        unread_count = notifications.filter(is_read=False).count()  
        notifications = notifications  

        return {
            'notifications': notifications,
            'unread_notifications_count': unread_count,
        }
    return {}
