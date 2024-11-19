from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import render, redirect
from user.models import User


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']


def home(req):
    return render(req, 'index.html')


def login_user(req):
    if req.POST:
        f_name = req.POST.get('name')
        f_password = req.POST.get('password')
        user = authenticate(req, name=f_name, password=f_password)
        if user is not None:
            login(req, user)
            return redirect('/')
        else:
            return redirect(req, '/login', {'error': 'Invalid username or password'})

    return render(req, 'login.html')


# user
# user@gnail.com

def register_user(req):
    if req.POST:
        form = CustomUserCreationForm(req.POST)

        if form.is_valid():
            f_email = form.cleaned_data['email']
            f_password = form.cleaned_data['password']
            f_password_confirmation = req.POST.get('password-confirmation')


            if f_password != f_password_confirmation:
                return render(req, 'register.html', {
                    'form': form,
                    'error': 'Password confirmation does not match the password.'
                })
            print(f_password != f_password_confirmation)

            if User.objects.filter(email=f_email).exists():
                return render(req, 'register.html', {
                    'form': form,
                    'error': 'User with this email already exists.'
                })

            user = form.save()
            login(req, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()

    return render(req, 'register.html', {'form': form})
