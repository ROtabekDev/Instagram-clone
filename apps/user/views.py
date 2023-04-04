import re

from django.contrib.contenttypes.models import ContentType
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
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve, reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.post.models import Post
from apps.main.models import Like
from apps.user.models import CustomUser, UserFollower
from apps.user.utils import phone_regex_pattern, email_regex_pattern, PhoneNumberBackend, EmailBackend
from django.db.models import Q, Count

from django.shortcuts import render
from .forms import EditProfileForm


def sign_in(request):
    if request.method == "POST":
        try:
            r = request.POST
            username = r['username']
            password = r['password']
            print(username, password)
            if re.match(phone_regex_pattern, username):
                user = authenticate(request, username=username, password=password, backend='core.backends.PhoneNumberBackend')
                print('phone', user)

            elif re.match(email_regex_pattern, username):
                user = authenticate(request, username=username, password=password, backend='core.backends.EmailBackend')
                print('email', user)
            else:
                user = authenticate(request, username=username, password=password)
                print('username', user)
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

        if re.match(phone_regex_pattern, phone_or_email):
            print('phone')
            user = authenticate(username=phone_or_email, password=password)
            print(user)
        elif re.match(email_regex_pattern, phone_or_email):
            print('email')
            user = authenticate(username=phone_or_email, password=password)
            print(user)
        else:
            print('username')
            user = authenticate(username=username, password=password)
            print(user)
        if user is not None:
            messages.error(request, f'{user} is already exist!')
            return redirect('sign-in')
        else:
            session = get_random_string(11)
            code = get_random_string(length=5, allowed_chars="0123456789")
            print("\n\n", code, "\n\n")
            user = {
                "username": username,
                "full_name": full_name,
                "phone_or_email": phone_or_email,
                "password": password
            }
            cache.set('user', user)
            cache.set('session', session)
            cache.set('code', code)
            return render(request, 'sms-code.html', {'code': code, 'session': session})
    return render(request, 'sign-up.html')
    #
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         messages.error(request, f'{user} is already exist!')
    #         return redirect('sign-in')
    #     else:
    #         session = get_random_string(11)
    #         code = get_random_string(length=5, allowed_chars="0123456789")
    #         print("\n\n", code, "\n\n")
    #         if re.match(phone_regex_pattern, phone_or_email):
    #             # user = CustomUser.objects.create(username=username, full_name=full_name, phone_number=phone_or_email, password=make_password(password), is_active=False)
    #             user = {
    #                 "username": username,
    #                 "full_name": full_name,
    #                 "phone_or_email": phone_or_email,
    #                 "password": password
    #             }
    #             cache.set('user', user, timeout=600)
    #             cache.set('session', session, timeout=600)
    #             cache.set('code', code, timeout=600)
    #         elif re.match(email_regex_pattern, phone_or_email):
    #             # user = CustomUser.objects.create(username=username, full_name=full_name, email=phone_or_email, password=make_password(password), is_active=False)
    #             user = {
    #                 "username": username,
    #                 "full_name": full_name,
    #                 "phone_or_email": phone_or_email,
    #                 "password": password
    #             }
    #             cache.set('user', user, timeout=600)
    #             cache.set('session', session, timeout=600)
    #             cache.set('code', code, timeout=600)
    #         else:
    #             messages.error(request, f'Enter SMS code')
    #         messages.error(request, f'{user} profile successfully created!')
    #
    #         return render(request, 'sms-code.html', {'code': code})
    # return render(request, 'sign-up.html')


def sms_code(request):
    if request.method == "POST":
        r = request.POST
        code = r['num1'] + r['num2'] + r['num3'] + r['num4'] + r['num5']
        user = cache.get('user')
        print(cache.get('session'), r['session'])
        print(cache.get('code'), code)
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

    #
    #     else:
    #         return redirect('sms-code')
    # session = get_random_string(11)
    # code = get_random_string(length=5, allowed_chars="0123456789")
    # cache.set('session', session, timeout=600)
    # cache.set('code', code, timeout=600)
    # print("\n\n", code, "\n\n")
    # return render(request, 'sms-code.html', {'code': code})


def sign_out(request):
    logout(request)

    return redirect('sign-in')


@login_required(redirect_field_name='next')
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
     
    self_profile= True if user==request.user else False
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
        
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['posts'] = Post.objects.filter(user_id__following__follower=self.request.user).exclude(
    #         user_id=self.request.user)
    #     return context


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
