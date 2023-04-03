import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.user.models import CustomUser, Participant, Chat, Message
from apps.user.utils import phone_regex_pattern, email_regex_pattern
from django.db.models import Q, Count


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

            return render(request, 'sms-code.html', {'code': code})
    return render(request, 'sign-up.html')


def sms_code(request):
    if request.method == "POST":
        r = request.POST
        code = r['num1'] + r['num2'] + r['num3'] + r['num4'] + r['num5']
        user = cache.get('user')
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
    context = {
        'user': get_object_or_404(CustomUser, username=username)
    }
    return render(request, 'profile.html', context)


@method_decorator(login_required, name='dispatch')
class MessageView(TemplateView):
    template_name = "message.html"

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        context['participants'] = Participant.objects.filter(~Q(user=self.request.user), chat__participant__user=self.request.user)
        context['all_users'] = CustomUser.objects.all().exclude(id=self.request.user.id)
        try:
            name = kwargs.get('name')
            chat = get_object_or_404(Chat, name=name)
            context['chat'] = chat
            context['partner'] = Participant.objects.filter(chat=chat).exclude(user=self.request.user).first()
            messages = chat.messages.all().filter(~Q(sender=self.request.user), is_read=False)
            for message in messages:
                message.is_read = True
                message.save()
        except Exception as e:
            pass
        return self.render_to_response(context)


def create_chat(request, user_id):
    chat = Chat.objects.filter(participant__user=request.user).filter(participant__user__id=user_id).distinct()
    if chat.exists():
        return redirect(f'/message/{chat.first().name}')
    else:
        chat = Chat.objects.create()
        Participant.objects.create(user_id=user_id, chat=chat)
        Participant.objects.create(user=request.user, chat=chat)

        return redirect(f'/message/{chat.name}')
