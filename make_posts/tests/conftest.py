import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import CommentFactory, PostFactory, UserFactory

register(UserFactory)
register(PostFactory)
register(CommentFactory)


@pytest.fixture
def api_client():
    return APIClient()
