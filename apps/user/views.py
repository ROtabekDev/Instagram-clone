import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.post.models import Post
from apps.user.models import CustomUser, UserFollower
from apps.user.utils import phone_regex_pattern, email_regex_pattern
from django.utils.crypto import get_random_string
from django.core.cache import cache


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
            session = get_random_string(11)
            code = get_random_string(length=5, allowed_chars="0123456789")
            print("\n\n", code, "\n\n")
            if re.match(phone_regex_pattern, phone_or_email):
                # user = CustomUser.objects.create(username=username, full_name=full_name, phone_number=phone_or_email, password=make_password(password), is_active=False)
                user = {
                    "username": username,
                    "full_name": full_name,
                    "phone_or_email": phone_or_email,
                    "password": password
                }
                cache.set('user', user, timeout=600)
                cache.set('session', session, timeout=600)
                cache.set('code', code, timeout=600)
            elif re.match(email_regex_pattern, phone_or_email):
                # user = CustomUser.objects.create(username=username, full_name=full_name, email=phone_or_email, password=make_password(password), is_active=False)
                user = {
                    "username": username,
                    "full_name": full_name,
                    "phone_or_email": phone_or_email,
                    "password": password
                }
                cache.set('user', user, timeout=600)
                cache.set('session', session, timeout=600)
                cache.set('code', code, timeout=600)
            else:
                messages.error(request, f'Enter SMS code')
            messages.error(request, f'{user} profile successfully created!')

            return render(request, 'sms-code.html', {'code': code })
    return render(request, 'sign-up.html')


def sms_code(request):
    if request.method == "POST":
        print('post keldi')
        r = request.POST
        code = r['num1'] + r['num2'] + r['num3'] + r['num4'] + r['num5']
        user = cache.get('user')
        print(user)
        # print(cache.get('session'), r['session'])
        # print(cache.get('code'), code)
        if cache.get('session') == r['session'] and cache.get('code') == code:
            if re.match(phone_regex_pattern, user['phone_or_email']):
                user = CustomUser.objects.create(username=user['username'], full_name=user['full_name'],
                                                 phone_number=user['phone_or_email'],
                                                 password=make_password(user['password']))
            elif re.match(email_regex_pattern, user['phone_or_email']):
                user = CustomUser.objects.create(username=user['username'], full_name=user['full_name'],
                                                 email=user['phone_or_email'], password=make_password(user['password']))
            print(user)
            return redirect('home')

        else:
            return redirect('sms-code')
    session = get_random_string(11)
    code = get_random_string(length=5, allowed_chars="0123456789")
    cache.set('session', session, timeout=600)
    cache.set('code', code, timeout=600)
    print("\n\n", code, "\n\n")
    return render(request, 'sms-code.html', {'code': code})


def sign_out(request):
    logout(request)

    return redirect('sign-in')


@login_required(redirect_field_name='next')
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username),
    self_profile= True if user[0]==request.user else False
    user_follow = UserFollower.objects.filter(follower=request.user, following=user[0]).exists() 
    
    context = {
        'user': get_object_or_404(CustomUser, username=username),
        'self_profile': self_profile,
        'user_follow': user_follow,
    }
    return render(request, 'profile.html', context)


@method_decorator(login_required, name='dispatch')
class MessageView(TemplateView):
    template_name = "message.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['posts'] = Post.objects.filter(user_id__following__follower=self.request.user).exclude(
    #         user_id=self.request.user)
    #     return context
