import factory
from factory.django import DjangoModelFactory
from make_posts.models import User, Post


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