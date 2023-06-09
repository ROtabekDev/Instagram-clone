import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import resolve, reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.main.models import Like
from apps.post.models import Post
from apps.user.models import CustomUser, UserFollower
from apps.user.models import Participant, Chat
from apps.user.utils import phone_regex_pattern, email_regex_pattern, send_sms_by_phone, send_sms_by_email
from .forms import EditProfileForm


def sign_in(request):
    if request.method == "POST":
        try:
            r = request.POST
            username = r['username']
            password = r['password']
            user = authenticate(request, username=username, password=password)
            if not user:
                user = authenticate(request, phone_number=username, password=password)
            elif not user:
                user = authenticate(request, email=username, password=password)

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
    try:
        global auth_type, result
        if request.method == "POST":
            r = request.POST
            phone_or_email = r['phone_or_email']
            full_name = r['full_name']
            username = r['username']
            password = r['password']
            if re.match(phone_regex_pattern, phone_or_email):
                user = authenticate(username=phone_or_email, password=password)
                auth_type = "phone"
            elif re.match(email_regex_pattern, phone_or_email):
                user = authenticate(username=phone_or_email, password=password)
                auth_type = "email"
            else:
                user = authenticate(username=username, password=password)
            if user is not None:
                messages.error(request, f'{user} is already exist!')
                return redirect('sign-in')
            else:
                session = get_random_string(11)
                code = get_random_string(length=5, allowed_chars="0123456789")
                user = {
                    "username": username,
                    "full_name": full_name,
                    "phone_or_email": phone_or_email,
                    "password": password
                }
                cache.set('user', user)
                cache.set('session', session)
                cache.set('code', code)
                if auth_type == "phone":
                    data = {
                        "mobile_phone": phone_or_email[1:],
                        "message": f"Your sms code : {code}.",
                        "from": 4546,
                        "callback_url": "https://uic.group"
                    }
                    result = send_sms_by_phone(data)
                elif auth_type == "email":
                    result = send_sms_by_email(phone_or_email, code)
                if result:
                    return render(request, 'sms-code.html', {'code': code, 'session': session})
                messages.error(request, "Phone number or email already exist!")
        return render(request, 'sign-up.html')
    except Exception as e:
        messages.error(f"{e}")
        return render(request, 'sign-up.html')


def sms_code(request):
    if request.method == "POST":
        r = request.POST
        code = r['num1'] + r['num2'] + r['num3'] + r['num4'] + r['num5']
        user = cache.get('user')
        if cache.get('session') == r['session'] and cache.get('code') == code:
            if re.match(phone_regex_pattern, user['phone_or_email']):
                user = CustomUser.objects.create(username=user['username'], full_name=user['full_name'],
                                                 phone_number=user['phone_or_email'],
                                                 password=make_password(user['password']))
            elif re.match(email_regex_pattern, user['phone_or_email']):
                user = CustomUser.objects.create(username=user['username'], full_name=user['full_name'],
                                                 email=user['phone_or_email'], password=make_password(user['password']))
            messages.success(request, f"{user} profile successfully created!")
            return redirect('sign-in')
    return redirect('sign-up')


def sign_out(request):
    logout(request)

    return redirect('sign-in')


@login_required(redirect_field_name='next')
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    self_profile = True if user == request.user else False
    user_follow = UserFollower.objects.filter(follower=request.user, following=user).exists()
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user_id=user).order_by('-created_at')

    if url_name == 'profile':
        posts = Post.objects.filter(user_id=user).order_by('-created_at')
    else:
        posts = user.saved_posts.all()

    context = {
        'user': get_object_or_404(CustomUser, username=username),
        'self_profile': self_profile,
        'user_follow': user_follow,
        'posts': posts
    }
    return render(request, 'profile.html', context)


@method_decorator(login_required, name='dispatch')
class MessageView(TemplateView):
    template_name = "message.html"

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        context['participants'] = Participant.objects.filter(~Q(user=self.request.user),
                                                             chat__participant__user=self.request.user)
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
            context['chat'] = Chat.objects.first()
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



@login_required(login_url='sign-in')
def follow(request, username):
    following = get_object_or_404(CustomUser, username=username)

    UserFollower.objects.update_or_create(follower=request.user, following=following)

    return redirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(reverse('profile', args=[username]))


@login_required(login_url='sign-in')
def unfollow(request, username):
    following = get_object_or_404(CustomUser, username=username)

    user_follow = UserFollower.objects.get(follower=request.user, following=following)
    user_follow.delete()

    return redirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(reverse('profile', args=[username]))


@login_required(login_url='sign-in')
def remove_follower(request, username):
    follower = get_object_or_404(CustomUser, username=username)

    user_follower = UserFollower.objects.get(following=request.user, follower=follower)
    user_follower.delete()

    return HttpResponseRedirect(reverse('profile', args=[request.user.username]))


@login_required(login_url='sign-in')
def remove_following(request, username):
    following = get_object_or_404(CustomUser, username=username)

    user_follower = UserFollower.objects.get(follower=request.user, following=following)

    user_follower.delete()

    return HttpResponseRedirect(reverse('profile', args=[request.user.username]))


@login_required(login_url='sign-in')
def create_like(request, post_id):
    content_type = ContentType.objects.get(model='post')
    post = content_type.model_class().objects.get(id=post_id)
    Like.objects.update_or_create(user_id=request.user, content_type=content_type, object_id=post.id)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='sign-in')
def remove_like(request, post_id):
    content_type = ContentType.objects.get(model='post')
    post = content_type.model_class().objects.get(id=post_id)
    like = Like.objects.get(user_id=request.user, content_type=content_type, object_id=post.id)
    like.delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='sign-in')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            # Redirect the user to their profile page
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})


def search_user(request):
    q = request.GET.get('q')
    users = CustomUser.objects.filter(username__icontains=q, full_name__icontains=q)
    data = serializers.serialize('json', users,
                                 fields=('id', 'username', 'avatar', 'full_name', 'last_activity', 'is_online'))
    return JsonResponse({'users': data})