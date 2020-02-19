import boto3
from functools import wraps
import errno
import os
import signal


def get_iam_client(profile=None):
    session = boto3.session.Session()

    client = session.client('iam')

    return client

def check_user(profile=None):
    session = boto3.session.Session(profile_name=profile)

    check = session.client('sts')

    return check.get_caller_identity()['Account']


class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, _handle_timeout)
                signal.alarm(seconds)
                try:
                    result = func(*args, **kwargs)
                finally:
                    signal.alarm(0)
                return result
            except ValueError as e:
                if str(e) == 'signal only works in main thread':
                    return func(*args, **kwargs)

        return wraps(func)(wrapper)

    return decorator
