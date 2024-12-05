from django.shortcuts import redirect
from django.urls import reverse

def auth_middleware(get_response):
    def middleware(request):
        # Define paths for better readability
        blogger_paths = ["/accounts/blogger_profile/", "/my_blogs/"]
        blogger_auth_paths = ["/accounts/blogger_register/", "/accounts/blogger_login/"]
        user_auth_paths = ["/accounts/user_register/", "/accounts/user_login/"]

        # Redirect if blogger is not logged in and trying to access blogger-specific pages
        if request.path in blogger_paths and request.session.get('blogger_id') is None:
            return redirect(reverse('index'))
        
        # Redirect if user is not logged in and trying to access blogger-specific pages
        elif request.path in blogger_paths and request.session.get('user_id') is None:
            return redirect(reverse('index'))  # Replace 'index' with your actual view name
        
        # Prevent logged-in bloggers from accessing blogger register/login pages
        if request.path in blogger_auth_paths and request.session.get('blogger_id') is not None:
            return redirect('/accounts/blogger_profile/')
        
        # Prevent logged-in users from accessing user register/login pages
        elif request.path in user_auth_paths and request.session.get('user_id') is not None:
            return redirect('/accounts/user_profile/')
        
        # Prevent logged-in users from accessing blogger register/login pages
        if request.path in blogger_auth_paths and request.session.get('user_id') is not None:
            return redirect('/accounts/user_profile/')
        
        # Prevent logged-in bloggers from accessing user register/login pages
        if request.path in user_auth_paths and request.session.get('blogger_id') is not None:
            return redirect('/accounts/blogger_profile/')
        
        # Allow the request to proceed if none of the above conditions match
        return get_response(request)

    return middleware
