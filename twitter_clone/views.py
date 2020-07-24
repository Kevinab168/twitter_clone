from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from make_posts.models import User, Post, Comment, Follow
from make_posts.forms import UserLoginForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
from django.views.generic.list import ListView
from django.views import View


class HomeView(TemplateView):
    template_name = 'index.html'


class LoginView(LoginView):
    template_name = 'log_in.html'
    authentication_form = UserLoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_page', request.user.pk)
        else:
            return super().get(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    template_name = 'user_page.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        return Post.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        context['form'] = PostForm
        context['searched_user'] = user
        context['following_number'] = Follow.objects.filter(follower=user).count()
        context['follower_number'] = Follow.objects.filter(following=user).count()
        return context


class PostFormView(FormView):
    template_name = 'user_page.html'
    form_class = PostForm

    def form_valid(self, form):
        post_text = form.cleaned_data.get('content')
        Post.objects.create(content=post_text, user=self.request.user)
        self.success_url = f'/users/{self.kwargs["user_id"]}'
        return super().form_valid(form)


class UserPageView(View):
    def get(self, request, *args, **kwargs):
        view = PostListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostFormView.as_view()
        return view(request, *args, **kwargs)


class CommentListView(ListView):
    model = Comment
    template_name = 'post_info.html'
    context_object_name = 'comments'

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Comment.objects.filter(post=post)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        context['post'] = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return context


class CommentFormView(FormView):
    template_name = 'post_info.html'
    form_class = CommentForm

    def form_valid(self, form):
        self.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        comment_content = form.cleaned_data.get('comment_content')
        Comment.objects.create(comment_content=comment_content, post=self.post, user=self.request.user)
        self.success_url = f'/posts/{self.kwargs["post_id"]}'
        return super().form_valid(form)


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        view = CommentListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentFormView.as_view()
        return view(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class FollowView(TemplateView):
    def get(self, request, *args, **kwargs):
        followed_user = get_object_or_404(User, pk=self.kwargs['user_id'])
        Follow.objects.get_or_create(follower=self.request.user, following=followed_user)
        return redirect('user_page', self.kwargs['user_id'])


class FollowersListView(ListView):
    model = Follow
    template_name = 'follower_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        followers = Follow.objects.filter(following=user)
        return followers

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['searched_user'] = get_object_or_404(User, pk=self.kwargs['user_id'])
        return context


class FollowingListView(ListView):
    model = Follow
    template_name = 'following_list.html'
    context_object_name = 'following'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        following = Follow.objects.filter(follower=user)
        return following

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['searched_user'] = get_object_or_404(User, pk=self.kwargs['user_id'])
        return context
