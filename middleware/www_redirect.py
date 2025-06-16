from django.http import HttpResponsePermanentRedirect


class WWWRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        # Redirect non-www domain to www
        if host == "shreebadapaliwalsamaj.com":
            new_url = f"https://www.shreebadapaliwalsamaj.com{request.get_full_path()}"
            return HttpResponsePermanentRedirect(new_url)
        return self.get_response(request)
