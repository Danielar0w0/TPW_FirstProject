from datetime import timezone

from django.shortcuts import render
from app.models import Post
from app.forms import PostForm


def layout(request):
    return render(request, 'layout.html')


def start_screen(request):
    return render(request, 'startScreen.html')


def feed(request):
    return render(request, 'feed.html')


def friends(request):
    return render(request, 'friends.html')


def profile2(request, user_email):
    params = {
        'posts': Post.objects.get(user_email=user_email)
    }

    return render(request, 'profile.html', params)


def profile(request):
    params = {
        'posts': Post.objects.all().order_by('-post_id')
    }

    return render(request, 'profile.html', params)


def create(request):

    if request.method == "POST" and 'file' in request.FILES:
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            user_email = "t@ua.pt"  #Hardcoded [TO CHANGE]
            description = request.POST["description"]
            file = request.FILES['file']

            if description and file:

                post = Post(user_email=user_email, description=description, file=file)
                post.save()

                return render(request, 'success.html')
    else:
        form = PostForm()

    return render(request, 'create.html', {"form": form})
