import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404

from apps.user.models import CustomUser
from apps.user.utils import phone_regex_pattern, email_regex_pattern


def sign_in(request):
    if request.method == "POST":
        try:
            r = request.POST
            username = r['username']
            password = r['password']

            if re.match(phone_regex_pattern, username):
                user = authenticate(request, phone_number=username, password=password)
            elif re.match(email_regex_pattern, username):
                user = authenticate(request, email=username, password=password)
            else:
                user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {user}')
                return redirect('home')
            else:
                messages.error(request, f"{user} is not found")
                return redirect('sign-in')

        except Exception as e:
            messages.error(request, f'{e}')
            return redirect('sign-in')
    return render(request, 'sign-in.html')


def sign_up(request):
    if request.method == "POST":
        r = request.POST
        phone_or_email = r['phone_or_email']
        full_name = r['full_name']
        username = r['username']
        password = r['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            messages.error(request, f'{user} is already exist!')
            return redirect('sign-in')
        else:
            if re.match(phone_regex_pattern, phone_or_email):
                user = CustomUser.objects.create(username=username, full_name=full_name, phone_number=phone_or_email,
                                                 password=make_password(password))
            elif re.match(email_regex_pattern, phone_or_email):
                user = CustomUser.objects.create(username=username, full_name=full_name, email=phone_or_email,
                                                 password=make_password(password))
            else:
                messages.error(request, f'{user} is not phone or email!')
            messages.error(request, f'{user} profile successfully created!')
            return redirect('sign-in')
    return render(request, 'sign-up.html')


def sign_out(request):
    logout(request)

    return redirect('sign-in')


@login_required(redirect_field_name='next')
def profile(request, username):
    context = {
        'user': get_object_or_404(CustomUser, username=username)
    }
    return render(request, 'profile.html', context)
