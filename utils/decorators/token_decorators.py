from rest_framework.response import Response


def is_not_token_valid(fn):
    def wrapper(object, request, **kwargs):
        print(object)
        if request.token is not None:
            if request.token == 'Not passed':
                return Response({'error': 'Token is not passed'}, status=400)
            if request.token == 'Need update':
                return Response({'error': 'Update token'}, status=400)
            return fn(object, request, **kwargs)

        else:
            return Response({'error': 'Token is not valid'}, status=400)
    return wrapper