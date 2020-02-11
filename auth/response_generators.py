from .serializers import UserSerializer


def gen_response(status: int = 200, meta: dict = None, body: dict = None) -> dict:
    if meta is None:
        meta = {}
    if body is None:
        body = {}
    response = {
        'head': {
            'status': status
        },
        'meta': meta,
        'body': body
    }
    return response


def gen_login_response(success: bool, user: UserSerializer) -> dict:
    error_message = ''
    if not success:
        error_message = 'The email or password provided are incorrect.'
    meta = {
        'loginSuccess': success,
        'errorMessage': error_message
    }
    body = user.data
    return gen_response(meta=meta, body=body)
