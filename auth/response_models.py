"""
This module provides utility functions for creating response dictionaries.
"""


def construct_response(status: int = 200, metadata: dict = None, body: dict = None):
    if metadata is None:
        metadata = dict()
    if body is None:
        body = dict()

    response_dict = {
        'head': {
            'status': status,
        },
        'meta': metadata,
        'body': body
    }
    return response_dict


def construct_login_response(success: bool):
    if success:
        error_message = ''
    else:
        error_message = 'The email or password entered is incorrect.'
    meta = {
        'loginSuccess': success,
        'errorMessage': error_message
    }
    return construct_response(metadata=meta)
