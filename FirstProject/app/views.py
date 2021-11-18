from datetime import timezone

from django.db.models import Q

from app.models import Post, User, Friendship
from django.shortcuts import render, redirect
from app.forms import PostForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from django.core.exceptions import ObjectDoesNotExist


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
    friends = Friendship.objects.filter(first_user=request.session['user'])
    return render(request, 'friends.html', {'users': friends})


@login_required(login_url='/login/')
def profile2(request, user_email):
    params = {
        'posts': Post.objects.get(user_email=user_email)
    }

    return render(request, 'profile.html', params)


@login_required(login_url='/login/')
def profile(request):
    user_email = request.session["user"]

    try:
        posts = Post.objects.filter(user_email=user_email)
    except ObjectDoesNotExist:
        posts = []

    params = {
        'posts': posts
    }

    return render(request, 'profile.html', params)


@login_required(login_url='/login/')
def create(request):
    if request.method == "POST" and 'file' in request.FILES:
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            user_email = request.session["user"]
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

            user_email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # Authenticate user
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # Save user if user is authenticated
            user = User(user_email=user_email, username=username, password=raw_password)
            user.save()

            # Save session
            request.session["user"] = user_email

            return render(request, 'startScreen.html')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def logout(request):
    request.session["user"] = ""
    return redirect('/login')


def search(request):
    if 'query' in request.POST:
        search_term = request.POST['query']
        if search_term:
            users = User.objects.filter(username__icontains=search_term).exclude(user_email=request.session['user'])
            friends = [f.second_user for f in Friendship.objects.filter(first_user=request.session['user'])]
            return render(request, 'search_results.html', {'users': users, 'friends': friends})

    if 'add_friend' in request.POST:
        friend = request.POST['add_friend']
        if friend:
            friends = Friendship.objects.filter(first_user=request.session['user'])
            if friend not in friends:
                friendship = Friendship(first_user=request.session['user'], second_user=friend)
                friendship.save()
                return redirect('/friends/')

    if 'remove_friend' in request.POST:
        friend = request.POST['remove_friend']
        if friend:
            friends = Friendship.objects.filter(first_user=request.session['user'], second_user=friend)
            for f in friends:
                f.delete()
            return redirect('/friends/')

    return render(request, 'search_results.html', {'users': []})