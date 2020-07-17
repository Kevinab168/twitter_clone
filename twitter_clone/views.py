from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from make_posts.models import User, Post
from make_posts.forms import UserLoginForm, PostForm


def homepage(request):
    return render(request, 'index.html')


def log_in(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user=user)
                return redirect('user_page', user.pk)
    userform = UserLoginForm()
    context = {'form': userform}
    return render(request, 'log_in.html', context)


def user_page(request, user_id):
    if request.method == 'POST':
        postform = PostForm(request.POST)
        if postform.is_valid():
            content = postform.cleaned_data.get('content')
            Post.objects.create(content=content, user=request.user)
    user = User.objects.get(pk=user_id)
    postform = PostForm()
    all_posts = Post.objects.filter(user=user)
    context = {
        'user': user,
        'form': postform,
        'posts': all_posts
    }
    return render(request, 'user_page.html', context)
