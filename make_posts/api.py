from rest_framework import filters, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework_extensions.routers import ExtendedDefaultRouter
from django_filters.rest_framework import DjangoFilterBackend


from .models import Comment, Follow, Image, Post, User
from .serializers import (CommentSerializer, FollowSerializerGet,
                          FollowSerializerPost, ImageSerializer,
                          PostSerializer, UserSerializer)


class PostViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('user').prefetch_related('comments').order_by('-created_at')
        if self.request.query_params.get('self', None):
            user = self.request.user
            return qs.filter(user=user)
        return qs


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('post', 'user').order_by('-created_at')
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['comment_content']
    filterset_fields = ['user']


class UserViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializerGet
    queryset = Follow.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('follower', 'following')

        keys = ['follower', 'following']
        user_id = None
        key = None
        while keys and not user_id:
            key = keys.pop()
            user_id = self.request.query_params.get(key)
        if key:
            user_id = self.request.query_params.get(key)
            get = {key + '__pk': user_id}
            qs = qs.filter(**get)
        return qs

    def get_serializer_class(self):
        serial_class = super().get_serializer_class()
        if self.request.method == 'POST':
            return FollowSerializerPost
        else:
            return serial_class


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


router = ExtendedDefaultRouter()
router.register(
    'api/posts', PostViewSet, basename='posts'
).register(
    'comments', CommentViewSet, basename='posts-comments', parents_query_lookups=['post']
)
router.register(
    'api/comments', CommentViewSet
)

router.register(
    'api/users', UserViewSet, basename='users'
).register(
    'posts', PostViewSet, basename='users-posts', parents_query_lookups=['user']
).register(
    'comments', CommentViewSet, basename='user-comments', parents_query_lookups=['post__user', 'post']
)

router.register('api/follows', FollowViewSet, basename='follow')
router.register('api/images', ImageViewSet)
