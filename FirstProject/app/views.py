from datetime import timezone

from django.db.models import Q

from app.models import Post, User, Comment, Friendship
from django.shortcuts import render, redirect
from app.forms import PostForm, RegisterForm, DeletePostForm, CommentForm
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

    # try:
    #    user = User.objects.get(user_email=user_email)
    # except ObjectDoesNotExist:
    #    return redirect('/login')

    user = User.objects.get(user_email=request.user.email)
    comment_form = CommentForm()

    try:
        posts = Post.objects.filter(user=user)
    except ObjectDoesNotExist:
        posts = []

    params = {
        'posts': posts,
        'form': comment_form
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
                user = User.objects.get(user_email=user_email)
                post = Post(user=user, description=description, file=file)
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
            user = authenticate(username=username, password=raw_password, )
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


def delete(request):
    if request.method == 'POST':
        form = DeletePostForm(request.POST)

        if form.is_valid():

            post_id = form.cleaned_data.get('post_id')
            post = Post.objects.get(post_id=post_id)

            # Delete post
            post.delete()

    return redirect('/profile')

def logout(request):
    request.session["user"] = ""
    return redirect('/login')



def search(request):
    if 'query' in request.POST:
        search_term = request.POST['query']
        if search_term:
            users = User.objects.filter(username__icontains=search_term).exclude(user_email=request.user.email)
            friends = [f.second_user for f in Friendship.objects.filter(first_user=request.user.email)]
            return render(request, 'search_results.html', {'users': users, 'friends': friends})

    if 'add_friend' in request.POST:
        friend = request.POST['add_friend']
        if friend:
            friends = Friendship.objects.filter(first_user=request.user.email)
            if friend not in friends:
                friendship = Friendship(first_user=request.user.email, second_user=friend)
                friendship.save()
                return redirect('/friends/')

    if 'remove_friend' in request.POST:
        friend = request.POST['remove_friend']
        if friend:
            friends = Friendship.objects.filter(first_user=request.user.email, second_user=friend)
            for f in friends:
                f.delete()
            return redirect('/friends/')

    return render(request, 'search_results.html', {'users': []})

def comment(request):

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():

            post_id = request.POST['post_id']
            user_email = request.POST['user_email']
            comment_content = form.cleaned_data.get('comment_content')

            user = User.objects.get(user_email=user_email)

            new_comment = Comment(post_id=post_id, content=comment_content, user=user)
            new_comment.save()

        return redirect('/profile')


def post_details(request, post_id):

    post = Post.objects.filter(post_id=post_id)[0]
    comments = Comment.objects.filter(post__post_id=post_id)

    params = {'post': post, 'comments': comments}

    return render(request, 'post_details.html', params)
