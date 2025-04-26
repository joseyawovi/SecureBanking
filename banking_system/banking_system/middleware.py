import time
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class SessionTimeoutMiddleware(MiddlewareMixin):
    """
    Middleware to handle session timeout
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            current_time = time.time()
            last_activity = request.session.get('last_activity')
            
            # Check if session has timed out
            if last_activity and current_time - last_activity > settings.SESSION_COOKIE_AGE:
                logout(request)
                messages.warning(request, 'Your session has expired. Please login again.')
                return redirect(settings.LOGIN_URL)
                
            # Update last activity time
            request.session['last_activity'] = current_time
