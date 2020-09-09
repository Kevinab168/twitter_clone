from django.urls import path

from make_posts import views

from .api import CustomObtainAuthToken, router

urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    path('login/', views.LoginView.as_view(), name='log_in'),
    path('users/<int:user_id>/', views.UserPageView.as_view(), name='user_page'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_info'),
    path('users/<int:user_id>/follow', views.FollowView.as_view(), name='follow'),
    path('users/<int:user_id>/followers', views.FollowersListView.as_view(), name='show_followers'),
    path('users/<int:user_id>/following', views.FollowingListView.as_view(), name='show_following'),
    path('home/', views.UserHomeView.as_view(), name='user_home'),
    path('search/', views.SearchView.as_view(), name='search_page'),
    path('search/users/', views.SearchUserView.as_view(), name='search_user_page'),
    path('search/posts/', views.SearchPostView.as_view(), name='search_post_page'),
    path('posts/<int:post_id>/edit', views.EditPostView.as_view(), name='edit_post'),
    path('posts/comments/<int:comment_id>/edit', views.EditCommentView.as_view(), name='edit_comment'),
    path('api/login/', CustomObtainAuthToken.as_view())
] + router.urls
