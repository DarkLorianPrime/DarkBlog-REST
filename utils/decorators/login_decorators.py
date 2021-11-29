from rest_framework.response import Response


def is_logged_in(fn):
    def wrapper(request, *args, **kwargs):
        if args[0].session.get('user') is None:
            return Response({'error': 'you not logged in'}, status=400)
        kwargs['key'] = args[0].session.get('name')
        return fn(request, *args, **kwargs)

    return wrapper


def is_not_logged_in(fn):
    def wrapper(request, *args, **kwargs):
        if args[0].session.get('name') is not None:
            return Response({'error': 'you already logged in'}, status=400)
        kwargs['key'] = args[0].session.get('name')
        return fn(request, *args, **kwargs)

    return wrapper