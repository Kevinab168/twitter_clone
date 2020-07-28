import factory
from factory.django import DjangoModelFactory
from make_posts.models import User, Post, Comment, Follow, Image


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    content = factory.Faker('sentence', nb_words=7)
    user = factory.SubFactory(UserFactory)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    comment_content = factory.Faker('sentence', nb_words=7)
    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)


class FollowFactory(DjangoModelFactory):
    class Meta:
        model = Follow

    follower = factory.SubFactory(UserFactory)
    following = factory.SubFactory(UserFactory)


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    source = factory.Faker('image_url')
    post = factory.SubFactory(PostFactory)
