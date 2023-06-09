from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from apps.user.models import CustomUser 

from .models import Post, PostFileContent, Hashtag, PostHastag, SavedPost

from apps.main.models import Comment, Like

from .forms import NewCommentForm


@login_required(login_url='sign-in')
def addpost(request):
    user = request.user 

    if request.method == 'POST':
        data = request.POST
        description = data['description']
        
        files = request.FILES.getlist('files')

        hashtags = [tag.strip("#") for tag in description.split() if tag.startswith("#")]
        new_description = ' '.join([word for word in description.split() if not word.startswith('#')])

        post = Post.objects.create(user_id=user, description=new_description)

        for file in files:
            PostFileContent.objects.create(
                post_id=post,
                file=file
            )

        for i in hashtags:
            tag = Hashtag.objects.get_or_create(tag_name=i)
            PostHastag.objects.create(post_id=post, tag_id=tag)
          
        return redirect("/")
 
    return render(request, 'post_create.html')



@login_required(login_url='sign-in')
def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    like_count = Like.objects.filter(content_type__model='post', object_id=post.id).count
    tags = PostHastag.objects.filter(post_id=post)
    comments = Comment.objects.filter(post_id=post).order_by('-created_at')


    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-detail', args=[post.id]))
    else:
        form = NewCommentForm()

    likes = Like.objects.filter(user_id=request.user).filter(content_type__model='post').values_list('object_id', flat=True).order_by('object_id')
    if likes.exists():
        like_indexes = list(likes)
    else:
        like_indexes = []


    posts = SavedPost.objects.filter(user_id=request.user).values_list('post_id', flat=True).order_by('post_id')
    
    if posts.exists():
        saved_posts = list(posts)
    else:
        saved_posts = []

    context = {
        'post': post,
        'like_count': like_count,
        'tags': tags,
        'form': form,
        'comments': comments,
        'like_indexes': like_indexes,
        'saved_posts': saved_posts
    }

    return render(request, 'post_detail.html', context)


@login_required(login_url='sign-in')
def deletepost(request, post_id): 

    Post.objects.filter(user_id=request.user, pk=post_id).delete() 

    return redirect('/')
    # return HttpResponseRedirect(reverse('profile', args=[username]))

@login_required(login_url='sign-in')
def create_savedpost(request, post_id):

    user = get_object_or_404(CustomUser, username=request.user.username)
    post = get_object_or_404(Post, id=post_id)
    SavedPost.objects.create(user_id=user, post_id=post)
   
    return redirect(request.META.get('HTTP_REFERER')) 


@login_required(login_url='sign-in')
def delete_savedpost(request, post_id):

    user = get_object_or_404(CustomUser, username=request.user.username)
    post = get_object_or_404(Post, id=post_id)
    SavedPost.objects.get(user_id=user, post_id=post).delete()
   
    return redirect(request.META.get('HTTP_REFERER')) 