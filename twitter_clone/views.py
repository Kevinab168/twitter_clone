from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from make_posts.models import User, Post, Comment, Follow, Image
from make_posts.forms import UserLoginForm, PostForm, CommentForm, ImageUploadForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
from django.views.generic.list import ListView
from django.views import View
from django.db.models import Count


class HomeView(TemplateView):
    template_name = 'index.html'


class UserHomeView(ListView):
    template_name = 'user_homepage.html'
    model = Post
    context_object_name = 'users_followed'

    def get_queryset(self, *args, **kwargs):
        return Follow.objects.filter(follower=self.request.user)


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
        context['img_form'] = ImageUploadForm
        context['searched_user'] = user
        context['following_number'] = Follow.objects.filter(follower=user).count()
        context['follower_number'] = Follow.objects.filter(following=user).count()
        return context


class PostFormView(FormView):
    template_name = 'user_page.html'
    form_class = PostForm

    def form_valid(self, form):
        files = self.request.FILES.getlist('source')
        post_text = form.cleaned_data.get('content')
        post = Post.objects.create(content=post_text, user=self.request.user)
        for file in files:
            Image.objects.create(source=file, post=post)
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
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        context['post'] = post
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


class EditPostView(FormView):
    template_name = 'edit.html'
    form_class = PostForm

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        post_text = form.cleaned_data.get('content')
        post.content = post_text
        post.save()
        self.success_url = f'/posts/{self.kwargs["post_id"]}'
        return super().form_valid(form)


class EditCommentView(FormView):
    template_name = 'edit.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = Comment.objects.get(pk=self.kwargs['comment_id'])
        comment_text = form.cleaned_data.get('comment_content')
        comment.comment_content = comment_text
        comment.save()
        self.success_url = f'/posts/{comment.post.pk}'
        return super().form_valid(form)


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


class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SearchUserView(FormView):
    template_name = 'search_user.html'
    form_class = SearchForm
    success_url = '/search/users/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form, *args, **kwargs):
        searched_query = form.cleaned_data.get('search_field')
        ordering = self.request.POST.get('order_results')
        user_search_results = User.objects.filter(username__icontains=searched_query) \
            .annotate(num_followers=Count('following')) \
            .order_by(ordering)
        context = super().get_context_data(**kwargs)
        context['search'] = searched_query
        context['user_results'] = user_search_results
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm
        return context


class SearchPostView(FormView):
    template_name = 'search_post.html'
    form_class = SearchForm
    success_url = '/search/posts/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form, *args, **kwargs):
        searched_query = str(form.cleaned_data.get('search_field'))
        ordering = self.request.POST.get('order_posts')
        post_search_results = Post.objects.filter(content__icontains=searched_query).order_by(ordering)
        context = super().get_context_data(**kwargs)
        context['search'] = searched_query
        context['post_results'] = post_search_results
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm
        return context
