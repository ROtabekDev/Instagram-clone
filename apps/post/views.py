from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 

from .models import Post, PostFileContent, Hashtag, PostHastag

@login_required(login_url='sign-in')
def addpost(request):
    user = request.user 

    if request.method == 'POST':
        data = request.POST
        description = data['description']
        
        files = request.FILES.getlist('files')
        print(data)
        post = Post.objects.create(user_id=user, description=description)

        for file in files:
            PostFileContent.objects.create(
                post_id=post,
                file=file
            )

        hashtags = [tag.strip("#") for tag in description.split() if tag.startswith("#")]
        
        for i in hashtags:
            tag = Hashtag.objects.create(tag_name=i)
            PostHastag.objects.create(post_id=post, tag_id=tag)
          
        return redirect("/")
 
    return render(request, 'post_create.html')