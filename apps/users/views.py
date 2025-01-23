from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def logout(request):
    auth_logout(request)
    return redirect("/")
