from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from user.models import User
from django.contrib import messages


class HomeDate:
    def __init__(self, space, used_space):
        self.space = space / 1024 ** 3 * 10
        self.used_space = used_space / 1024 ** 3 * 10


def check_auth(req, page):
    if req.user.is_authenticated:
        return redirect('/')
    return render(req, f'{page}.html')


def home(req):
    if not req.user.is_authenticated:
        return redirect('login')

    home_data = HomeDate(space=req.user.space, used_space=req.user.used_space)
    return render(req, 'index.html', {'home_data': home_data})


def login_user(req):
    if req.POST:
        f_username = req.POST.get('username')
        f_password = req.POST.get('password')

        user = authenticate(username=f_username, password=f_password)
        if user is not None:
            login(req, user)
            return redirect('/')
        else:
            if not User.objects.filter(username=f_username).exists():
                messages.error(req, 'User with this username not exists')
            else:
                messages.error(req, 'Invalid password entered')

    return check_auth(req, 'login')


def register_user(req):
    if req.POST:
        f_username = req.POST.get('username')
        f_email = req.POST.get('email')
        f_password1 = req.POST.get('password1')
        f_password2 = req.POST.get('password2')

        if not f_username or not f_email or not f_password1 or not f_password2:
            messages.error(req, 'Please fill in all the fields below')
        elif f_password1 != f_password2:
            messages.error(req, 'Password confirmation does not match the password')
        elif User.objects.filter(email=f_email).exists() or User.objects.filter(username=f_username).exists():
            messages.error(req, 'User with this username or email already exists')

        if messages.get_messages(req):
            return render(req, 'register.html')

        user = User.objects.create_user(username=f_username, email=f_email, password=f_password1)
        user.save()
        login(req, user)

    return check_auth(req, 'register')
