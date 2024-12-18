from collections.abc import Callable

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def simple_view(template_name: str) -> Callable[[HttpRequest], HttpResponse]:
    return login_required(lambda request: render(request, template_name))


@login_required
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/home.html')


@login_required
def search(_request: HttpRequest) -> HttpResponse:
    return redirect('storage-search')
    # return render(request, 'core/search.html')


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('user-login')


def login_user(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        context = {
            'redirect_page': request.GET.get('next') or '/',
            'invalid_credentials': False,
        }
        return render(request, 'core/login.html', context)

    redirect_page = request.POST.get('redirect_page') or '/'
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user is None:
        context = {
            'redirect_page': redirect_page,
            'invalid_credentials': True,
        }
        return render(request, 'core/login.html', context)

    login(request, user)
    return redirect(redirect_page)
