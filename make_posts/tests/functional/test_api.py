from make_posts.models import User


def test_login_response(db, api_client):
    User.objects.create_user(username='test', password='test')
    response = api_client.post('/api/login/', data={'username': 'test', 'password': 'test'})
    assert response.status_code == 200


def test_post_api(db, post_factory, api_client):
    POST_COUNT = 20
    for post in range(POST_COUNT):
        post_factory.create()
    response = api_client.get('/api/posts/', format='json')
    assert response.status_code == 200
    assert len(response.json()) == 20


def test_user_api(db, user_factory, api_client):
    USER_COUNT = 20
    for user in range(USER_COUNT):
        user_factory.create()
    response = api_client.get('/api/users/', format='json')
    assert response.status_code == 200
    assert len(response.json()) == 20


def test_comment_api(db, comment_factory, api_client):
    COMMENT_COUNT = 20
    for comment in range(COMMENT_COUNT):
        comment_factory.create()
    response = api_client.get('/api/comments/', format='json')
    assert response.status_code == 200
    assert len(response.json()) == 20


def test_api_search_user(db, user_factory, api_client):
    SEARCH_QUERY = 'test'
    user_factory.create(username=SEARCH_QUERY)
    response = api_client.get(f'/api/users/?username={SEARCH_QUERY}', format='json')
    user_list = response.json()
    assert response.status_code == 200
    assert len(user_list) == 1
    assert user_list[0].get('username') == 'test'


def test_api_add_post(db, user_factory, api_client):
    user = user_factory.create()
    POST = {
        'content': 'test',
        'user': user.id
    }
    response = api_client.post('/api/posts/', POST, format='json')
    created_post = response.json()
    assert response.status_code == 201
    assert created_post.get('content') == POST.get('content')
    assert created_post.get('user') == POST.get('user')


def test_api_add_comment(db, user_factory, post_factory, api_client):
    user = user_factory.create()
    post = post_factory.create()
    COMMENT = {
        'comment_content': 'test',
        'post': post.id,
        'user': user.id
    }
    response = api_client.post('/api/comments/', COMMENT, format='json')
    created_comment = response.json()
    assert response.status_code == 201
    assert created_comment.get('comment_content') == COMMENT.get('comment_content')
    assert created_comment.get('post') == COMMENT.get('post')
    assert created_comment.get('user') == COMMENT.get('user')


def test_api_search_post(db, post_factory, api_client):
    POST = 'test 12'
    post_factory.create(content=POST)
    response = api_client.get(f'/api/posts/?search={POST}', format='json')
    response_post_list = response.json()
    assert len(response_post_list) == 1
    assert response.status_code == 200
    assert response_post_list[0].get('content') == POST
