import json

from django.http import HttpResponse


def report_authorization(view):
    def wrapper(*args, **kwargs):
        request = args[0]
        return view(request)
        if request.user and request.user.is_superuser:
            return view(request)
        else:
            return HttpResponse(json.dumps({"message": "Unauthorized"}), status=403)

    return wrapper
