from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


@login_required
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/home.html')


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.info(request, 'Logout successful')
    return redirect('user-login')


def login_user(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        context = {'redirect_page': request.GET.get('next', '/')}
        return render(request, 'core/login.html', context)

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is None:
        messages.error(request, 'Invalid credentials, try again')
        return redirect('user-login')

    login(request, user)
    messages.success(request, 'Login successful!')
    return redirect(request.POST.get('redirect_page') or '/')
