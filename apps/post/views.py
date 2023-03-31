from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse 

from .models import Post, PostFileContent, Hashtag, PostHastag

from apps.main.models import Comment, Like

from .forms import NewCommentForm


@login_required(login_url='sign-in')
def addpost(request):
    user = request.user 

    if request.method == 'POST':
        data = request.POST
        description = data['description']
        
        files = request.FILES.getlist('files')
        print(data)

        hashtags = [tag.strip("#") for tag in description.split() if tag.startswith("#")]
        new_description = ' '.join([word for word in description.split() if not word.startswith('#')])

        post = Post.objects.create(user_id=user, description=new_description)

        for file in files:
            PostFileContent.objects.create(
                post_id=post,
                file=file
            )

        for i in hashtags:
            tag = Hashtag.objects.create(tag_name=i)
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

    context = {
        'post': post,
        'like_count': like_count,
        'tags': tags,
        'form': form,
        'comments': comments
    }

    return render(request, 'post_detail.html', context)