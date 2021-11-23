from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from app.forms import PostForm, RegisterForm, DeletePostForm, CommentForm, ProfileImageForm, ProfilePasswordForm, \
    MessageForm
from app.models import Post, User, Comment, Friendship, Message


def layout(request):
    return render(request, 'layout.html')


@login_required(login_url='/login/')
def start_screen(request):

    if request.user not in User.objects.all() and request.user.is_superuser:
        user = User(username=request.user.username, user_email=request.user.email, password=request.user.password, admin=True)
        user.save()

    user = User.objects.get(user_email=request.user.email)
    return render(request, 'startScreen.html', {'user': user})


@login_required(login_url='/login/')
def feed(request):

    all_posts = []
    comments_form = CommentForm()
    all_messages = []


    current_user = User.objects.get(user_email=request.user.email)
    friends_join = Friendship.objects.select_related('first_user', 'second_user').filter(first_user=current_user)

    for friend_row in friends_join:
        friend_posts = Post.objects.filter(user=friend_row.second_user)
        all_posts.extend(friend_posts)

        friend_messages = Message.objects.filter(sender=current_user, receiver=friend_row.second_user)
        all_messages.extend(friend_messages)

    return render(request, 'feed.html', {'posts': all_posts, 'messages': all_messages, 'comment_form': comments_form, 'user': current_user})


@login_required(login_url='/login/')
def friends(request):

    user = User.objects.get(user_email=request.user.email)
    friends = Friendship.objects.filter(first_user__user_email=request.user.email)
    users = []
    for friend in friends:
        users.append(friend.second_user)

    return render(request, 'friends.html', {'users': users, 'user': user})


@login_required(login_url='/login/')
def profile(request):

    user = User.objects.get(user_email=request.user.email)
    following = len(Friendship.objects.filter(first_user=user))
    followers = len(Friendship.objects.filter(second_user=user))
    comment_form = CommentForm()

    try:
        posts = Post.objects.filter(user=user)
    except ObjectDoesNotExist:
        posts = []

    params = {
        'user': user,
        'user_profile': user,
        'posts': posts,
        'form': comment_form,
        'following': following,
        'followers': followers
    }

    return render(request, 'profile.html', params)


@login_required(login_url='/login/')
def edit_profile(request):

    success = False
    user = User.objects.get(user_email=request.user.email)

    # Image
    if request.method == "POST" and 'image' in request.FILES:

        form = ProfileImageForm(request.POST, request.FILES)

        if form.is_valid():

            file = request.FILES['image']

            if file:
                user.image = file
                user.update_image(file)
                user.save()

                success = True

    # Password
    if request.method == "POST" and 'password' in request.POST:

        form = ProfilePasswordForm(request.POST)

        if form.is_valid():

            password = request.POST['password']

            if password:

                request.user.set_password(password)
                request.user.save()

                user.update_password(password)
                user.save()

                success = True

    if not success:

        form_image = ProfileImageForm()
        form_password = ProfilePasswordForm()

        return render(request, 'edit_profile.html', {'formImage': form_image, 'formPassword': form_password, 'user': user})

    return redirect("/profile/")


@login_required(login_url='/login/')
def create(request):

    user = User.objects.get(user_email=request.user.email)

    if request.method == "POST" and 'file' in request.FILES:
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            user_email = request.user.email
            description = request.POST["description"]
            file = request.FILES['file']

            if description and file:
                user = User.objects.get(user_email=user_email)
                post = Post(user=user, description=description, file=file)
                post.save()

                return render(request, 'success.html')
    else:
        form = PostForm()

    return render(request, 'create.html', {"form": form, 'user': user})


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
            user = User(user_email=user_email, username=username, password=raw_password, image="user2.png")
            user.save()

            return render(request, 'startScreen.html', {"user": user})
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required(login_url='/login/')
def delete(request):
    if request.method == 'POST':
        form = DeletePostForm(request.POST)

        if form.is_valid():

            post_id = form.cleaned_data.get('post_id')
            post = Post.objects.get(post_id=post_id)

            # Delete post
            post.delete()

    return redirect('/profile')


@login_required(login_url='/login/')
def logout(request):
    return redirect('/login')


@login_required(login_url='/login/')
def search(request):

    user = User.objects.get(user_email=request.user.email)
    if 'query' in request.POST:

        search_term = request.POST['query']

        if search_term:

            users = User.objects.filter(username__icontains=search_term).exclude(user_email=request.user.email)
            friends = [f.second_user for f in Friendship.objects.filter(first_user=request.user.email)]

            return render(request, 'search_results.html',
                          {'users': users, 'friends': friends, 'search_term': search_term, 'user': user})

    if 'add_friend' in request.POST:

        friend = request.POST['add_friend']

        if friend:

            current_user = User.objects.get(user_email=request.user.email)
            friend_user = User.objects.get(user_email=friend)

            friends = Friendship.objects.filter(first_user=current_user)

            if friend not in friends:
                friendship = Friendship(first_user=current_user, second_user=friend_user)
                friendship.save()
                return redirect('/friends/')

    if 'remove_friend' in request.POST:

        friend = request.POST['remove_friend']

        if friend:

            current_user = User.objects.get(user_email=request.user.email)
            friend_user = User.objects.get(user_email=friend)

            friends = Friendship.objects.filter(first_user=current_user, second_user=friend_user)

            for f in friends:
                f.delete()
            return redirect('/friends/')

    if 'query_friend' in request.POST:

        search_term = request.POST['query_friend']

        if search_term:
            # search by username
            users = User.objects.filter(username__icontains=search_term).exclude(user_email=request.user.email)
            current_user = User.objects.get(user_email=request.user.email)

            friends = []

            for user in users:
                friend = Friendship.objects.filter(first_user=current_user, second_user=user)
                if friend:
                    friends.append(user)
            return render(request, 'friends.html', {'users': friends, 'user': user})

        return redirect('/friends/')

    return render(request, 'search_results.html', {'users': [], 'user': user})


@login_required(login_url='/login/')
def comment(request):

    if request.method == 'POST':

        form = CommentForm(request.POST)
        redirect_uri = '/profile'

        if form.is_valid():

            if 'redirect_uri' in request.POST:
                redirect_uri = request.POST['redirect_uri']

            post_id = request.POST['post_id']
            comment_content = form.cleaned_data.get('comment_content')

            user = User.objects.get(user_email=request.user.email)

            new_comment = Comment(post_id=post_id, content=comment_content, user=user)
            new_comment.save()

        return redirect(redirect_uri)


def post_details(request, post_id):

    user = None
    if request.user.is_authenticated:
        user = User.objects.get(user_email=request.user.email)

    post = Post.objects.filter(post_id=post_id)[0]
    comments = Comment.objects.filter(post__post_id=post_id)

    params = {'post': post, 'comments': comments, 'user': user}

    return render(request, 'post_details.html', params)


@login_required(login_url='/login/')
def messages(request):
    user = User.objects.get(user_email=request.user.email)
    friends = Friendship.objects.filter(first_user__user_email=request.user.email)

    users = []
    for friend in friends:
        if friend.second_user not in users:
            users.append(friend.second_user)

    friends = Friendship.objects.filter(second_user__user_email=request.user.email)
    for friend in friends:
        if friend.first_user not in users:
            users.append(friend.first_user)

    return render(request, 'messages.html', {"users": users, 'user': user})


@login_required(login_url='/login/')
def messages_with(request, username):

    user = User.objects.get(user_email=request.user.email)

    if request.method == 'POST':

        form = MessageForm(request.POST)

        if form.is_valid():
            content = request.POST['content']
            other_user = User.objects.get(username=request.POST['other_user'])
            current_user = User.objects.get(username=request.user.username)

            message = Message(sender=current_user, receiver=other_user, content=content)
            message.save()

    else:

        form = MessageForm()

    other_user = User.objects.get(username=username)
    messages_with_user = Message.objects.filter(Q(receiver__username=username, sender__username=request.user.username) | \
                         Q(receiver__username=request.user.username, sender__username=username))

    params = {
        'form': form,
        'user': user,
        'current_user': request.user.username,
        'other_user': other_user,
        'messages': messages_with_user
    }

    return render(request, 'messages_with.html', params)


def user_profile(request, email):

    try:
        user = User.objects.get(user_email=email)
    except ObjectDoesNotExist:
        return render(request, 'not_found.html', {'message': 'User not found'})

    comment_form = CommentForm()
    following = len(Friendship.objects.filter(first_user=user))
    followers = len(Friendship.objects.filter(second_user=user))
    user_friends = []
    current_user = None

    if request.user.is_authenticated:

        current_user = User.objects.get(user_email=request.user.email)
        user_friendships = Friendship.objects.filter(first_user=current_user)

        for user_friendship in user_friendships:
            user_friends.append(user_friendship.second_user)

    try:
        posts = Post.objects.filter(user=user)
    except ObjectDoesNotExist:
        posts = []

    params = {
        'user': current_user,
        'user_profile': user,
        'posts': posts,
        'user_friends': user_friends,
        'form': comment_form,
        'following': following,
        'followers': followers
    }

    return render(request, 'profile.html', params)


@login_required(login_url='/login/')
def unfollow_user(request, email):

    if request.method == 'POST':

        current_user = User.objects.get(user_email=request.user.email)

        try:
            user_to_unfollow = User.objects.get(user_email=email)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('Could not find the user {}.'.format(email))

        try:
            friendship_to_remove = Friendship.objects.get(first_user=current_user, second_user=user_to_unfollow)
            friendship_to_remove.delete()
        except ObjectDoesNotExist:
            return HttpResponseNotFound('You are not following that user.')

        return HttpResponse(content='You have unfollowed {}.'.format(user_to_unfollow.username), content_type='text/plain')


@login_required(login_url='/login/')
def admin_panel(request):

    user = User.objects.get(user_email=request.user.email)
    if user.admin:
        posts = Post.objects.all()
        return render(request, 'admin_panel.html', {'posts': posts, 'user': user})

    return redirect('/profile/')