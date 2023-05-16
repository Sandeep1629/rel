# from django.shortcuts import redirect
# from django.urls import reverse
# from datetime import datetime, timedelta
#
# class SessionTimeoutMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             last_activity = request.session.get('last_activity')
#             if last_activity:
#                 now = datetime.now()
#                 if now > last_activity + timedelta(seconds=settings.SESSION_EXPIRE_SECONDS):
#                     print("sess")
#                     # The session has expired, redirect to the login page
#                     return redirect(reverse('home'))
#
#             # Update the last activity time in the session
#             request.session['last_activity'] = datetime.now()
#
#         response = self.get_response(request)
#
#         return response