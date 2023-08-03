from functools import wraps

def check_end_status(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        request.end_status = request.session.get('end_status', False)
        return f(request, *args, **kwargs)
    return wrap