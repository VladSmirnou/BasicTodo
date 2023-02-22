from django.shortcuts import redirect


def login_request_check(not_=None):
    def outer(func):
        def assert_credentials(*args, **kwargs):
            if not not_:
                if args[1].user.is_authenticated and args[1].htmx:
                    return func(*args, **kwargs)
                return redirect('home_page')
            if not args[1].user.is_authenticated and args[1].htmx:
                return func(*args, **kwargs)
            return redirect('home_page')
        return assert_credentials
    return outer