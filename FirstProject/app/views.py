from datetime import timezone

from django.shortcuts import render
from app.models import Post, User, Friendship
from app.forms import PostForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate


def layout(request):
    return render(request, 'layout.html')


@login_required(login_url='/login/')
def start_screen(request):
    return render(request, 'startScreen.html')


@login_required(login_url='/login/')
def feed(request):
    return render(request, 'feed.html')


@login_required(login_url='/login/')
def friends(request):
    return render(request, 'friends.html')

@login_required(login_url='/login/')
def profile2(request, user_email):
    params = {
        'posts': Post.objects.get(user_email=user_email)
    }

    return render(request, 'profile.html', params)

@login_required(login_url='/login/')
def profile(request):
    params = {
        'posts': Post.objects.all().order_by('-post_id')
    }

    return render(request, 'profile.html', params)

@login_required(login_url='/login/')
def create(request):
    if request.method == "POST" and 'file' in request.FILES:
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            user_email = "t@ua.pt"  # Hardcoded [TO CHANGE]
            description = request.POST["description"]
            file = request.FILES['file']

            if description and file:
                post = Post(user_email=user_email, description=description, file=file)
                post.save()

                return render(request, 'success.html')
    else:
        form = PostForm()

    return render(request, 'create.html', {"form": form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user = User(user_email=form.cleaned_data.get('email'), username=username, password=raw_password)
            user.save()
            return render(request,'startScreen.html')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



