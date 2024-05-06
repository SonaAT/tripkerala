from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Add the URLs that should be accessible without authentication
        self.allowed_urls = [reverse('signin'), reverse('signup')]  # Add 'signup' or any other URL

    def __call__(self, request):
        response = self.get_response(request)
        # Check if the requested URL is in the allowed URLs list
        if not request.user.is_authenticated and request.path not in self.allowed_urls:
            # Redirect to the signin page if not authenticated
            response = redirect('signin')
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        else:
            # If user is authenticated, ensure no caching of sensitive pages
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
