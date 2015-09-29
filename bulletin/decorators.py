from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.utils.six.moves.urllib.parse import urlparse


def user_passes_test(function=None,
                     test_func=None,
                     redirect_field_name=REDIRECT_FIELD_NAME,
                     fail_url=None):
    """Similar to user_passes_test in django.contrib.auth except this one
    can be used like this:

        f = user_passes_test(f)

    Decorator for views that checks that the user passes the given test,
    redirecting to `fail_url` for failures. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            # urlparse chokes on lazy objects in Python 3, force to str
            resolved_fail_url = force_str(resolve_url(fail_url))
            # If the fail url is the same scheme and net location then just
            # use the path as the "next" url.
            fail_scheme, fail_netloc = urlparse(resolved_fail_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not fail_scheme or fail_scheme == current_scheme) and
                (not fail_netloc or fail_netloc == current_netloc)):
                path = request.get_full_path()
            return redirect(fail_url)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator
