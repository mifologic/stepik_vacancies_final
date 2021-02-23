def get_current_user(request):
    return request.user if request.user.is_authenticated else None
