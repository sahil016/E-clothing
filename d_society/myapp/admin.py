from django.contrib import admin
from .models import *
from django.contrib.sessions.models import Session
from django.utils.timezone import now
import json
# Register your models here.



def is_user_logged_in(user):
    """Check if the user has an active session."""
    sessions = Session.objects.filter(expire_date__gte=now())
    for session in sessions:
        data = session.get_decoded()
        if str(user.id) in json.dumps(data):  # Check if user ID is in session data
            return True
    return False

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_logged_in', 'is_active']
    search_fields = ['username', 'email']

    def is_logged_in(self, obj):
        """Check if the user has an active session"""
        sessions = Session.objects.filter(expire_date__gte=now())  # Get all active sessions
        for session in sessions:
            data = session.get_decoded()
            if str(obj.id) == str(data.get('_auth_user_id')):  # Check if user is in session
                return True
        return False

    is_logged_in.boolean = True  # Displays a checkmark (✔️) instead of True/False
    is_logged_in.short_description = "Logged In"

admin.site.register(User, UserAdmin)
admin.site.register(Chairman)
admin.site.register(Watchman)
admin.site.register(Member)
admin.site.register(Visitor)
admin.site.register(Notice)
admin.site.register(Event)