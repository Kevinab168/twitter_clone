"""twitter_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='homepage'),
    path('login/', views.LoginView.as_view(), name='log_in'),
    path('users/<int:user_id>/', views.UserPageView.as_view(), name='user_page'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_info'),
    path('users/<int:user_id>/follow', views.FollowView.as_view(), name='follow'),
    path('users/<int:user_id>/followers', views.FollowersListView.as_view(), name='show_followers'),
    path('users/<int:user_id>/following', views.FollowingListView.as_view(), name='show_following'),
    path('home/', views.UserHomeView.as_view(), name='user_home'),
    path('search/', views.SearchView.as_view(), name='search_page'),
    path('search/posts/', views.SearchPostView.as_view(), name='search_post_page'),
]
