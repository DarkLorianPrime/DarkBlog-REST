from rest_framework.response import Response


def is_logged_in(fn):
    def wrapper(self, request):
        if request.headers.get('Authorization') is None:
            return Response({'error': 'you not logged in'}, status=400)
        return fn(self, request)

    return wrapper


def is_not_logged_in(fn):
    def wrapper(self, request):
        if request.headers.get('Authorization') is not None:
            return Response({'error': 'you not logged in'}, status=400)
        return fn(self, request)

    return wrapper