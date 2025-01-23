import time


class SessionCreationTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and "_creation_time" not in request.session:
            request.session["_creation_time"] = time.time()

        response = self.get_response(request)
        return response
