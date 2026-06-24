from django.shortcuts import redirect

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        allowed_urls = [
            "/",
            "/register-page/",
            "/api/login/",
            "/api/token/refresh/",
        ]

        # allow public URLs
        if request.path in allowed_urls:
            return self.get_response(request)

        # check login
        if not request.user.is_authenticated:
            return redirect("/")

        return self.get_response(request)