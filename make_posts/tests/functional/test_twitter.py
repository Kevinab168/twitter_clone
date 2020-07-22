from pytest_factoryboy import register
from make_posts.tests.factories import UserFactory, PostFactory, FollowFactory
from make_posts.models import Post, Comment, Follow

register(UserFactory)
register(PostFactory)
register(FollowFactory)


def test_landing_page(driver, live_server):
    driver.get(live_server.url)
    assert "welcome" in driver.page_source.lower()
    assert driver.find_element_by_css_selector('[data-test="login-link"]')


def test_login_page(driver, live_server, user_factory):
    user = user_factory.create()
    user.set_password('test')
    user.save()
    driver.get(live_server.url + '/login')
    username_input = driver.find_element_by_css_selector('[data-test="username"]')
    username_input.send_keys(user.username)
    password_input = driver.find_element_by_css_selector('[data-test="password"]')
    password_input.send_keys('test')
    log_in = driver.find_element_by_css_selector('[data-test="log-in"]')
    log_in.click()
    assert user.username in driver.find_element_by_css_selector('[data-test="user"]').text
    assert driver.find_element_by_css_selector('[data-test="follower-count"]')
    assert driver.find_element_by_css_selector('[data-test="following-count"]')
    assert driver.find_element_by_css_selector('[data-test="make-post"]')


def test_make_post(driver, login_user, live_server, user_factory):
    user = user_factory.create()
    login_user(user)
    driver.get(live_server.url + f'/users/{user.pk}')
    post_text = driver.find_element_by_css_selector('[data-test="post"]')
    post_text.send_keys('Sample Post')
    post_it = driver.find_element_by_css_selector('[data-test="make-post"]')
    post_it.click()
    assert 'Sample Post' in driver.find_element_by_css_selector('[data-test="created-post"]').text
    last_post = Post.objects.all().last()
    assert last_post.user == user


def test_make_comment(driver, live_server, login_user, user_factory, post_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(10):
        post_factory.create(user=user)
    post_1 = Post.objects.get(pk=1)
    driver.get(live_server + f'/posts/{post_1.pk}')
    comment_field = driver.find_element_by_css_selector('[data-test="comment-text"]')
    comment_field.send_keys('Sample1')
    submit_comment = driver.find_element_by_css_selector('[data-test="create-comment"]')
    submit_comment.click()
    assert 'Sample1' in driver.find_element_by_css_selector('[data-test="user-comment"]').text
    recent_comment = Comment.objects.all().last()
    assert recent_comment.user == user
    assert recent_comment.post == post_1


def test_follow_change(driver, live_server, login_user, user_factory, post_factory):
    user = user_factory.create()
    user2 = user_factory.create()
    login_user(user2)
    driver.get(live_server.url + f'/users/{user.pk}')
    follow_button = driver.find_element_by_css_selector('[data-test="follow"]')
    follow_button.click()
    follower_count = driver.find_element_by_css_selector('[data-test="follower-count"]').text
    assert '1' in follower_count
    following_count = driver.find_element_by_css_selector('[data-test="following-count"]').text
    assert '0' in following_count
    follow = Follow.objects.all().last()
    assert follow.follower == user2
    assert follow.following == user


def test_see_followers(driver, live_server, login_user, user_factory, follow_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(20):
        follow_factory.create(following=user)
    driver.get(live_server.url + f'/users/{user.pk}/followers')
    followers_list = driver.find_elements_by_css_selector('[data-test="followers"]')
    followers_count = 20
    assert len(followers_list) == followers_count
    assert 'Followers' in driver.find_element_by_css_selector('[data-test="follower-page-heading"]').text
    first_follower = Follow.objects.get(pk=1)
    assert first_follower.following == user


def test_go_to_follower_homepage(driver, live_server, login_user, user_factory, follow_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(20):
        follow_factory.create(following=user)
    driver.get(live_server.url + f'/users/{user.pk}/followers')
    follower_homepage = driver.find_element_by_css_selector('[data-test="follower-homepage"]')
    follower_homepage.click()
    first_follower = Follow.objects.get(pk=1)
    assert first_follower.follower.username in driver.find_element_by_css_selector('[data-test="user"]').text
    assert driver.find_element_by_css_selector('[data-test="follower-count"]')
    assert driver.find_element_by_css_selector('[data-test="following-count"]')


def test_see_following(driver, live_server, login_user, user_factory, follow_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(20):
        follow_factory.create(follower=user)
    driver.get(live_server.url + f'/users/{user.pk}/following')
    following_list = driver.find_elements_by_css_selector('[data-test="following"]')
    following_count = 20
    assert len(following_list) == following_count
    assert 'Following' in driver.find_element_by_css_selector('[data-test="following-page-heading"]').text
    first_user_followed = Follow.objects.get(pk=1)
    assert first_user_followed.follower == user


def test_go_to_following_homepage(driver, live_server, login_user, user_factory, follow_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(20):
        follow_factory.create(follower=user)
    driver.get(live_server.url + f'/users/{user.pk}/following')
    following_homepage = driver.find_element_by_css_selector('[data-test="following-homepage"]')
    following_homepage.click()
    first_user_followed = Follow.objects.get(pk=1)
    assert first_user_followed.following.username in driver.find_element_by_css_selector('[data-test="user"]').text
    assert driver.find_element_by_css_selector('[data-test="follower-count"]')
    assert driver.find_element_by_css_selector('[data-test="following-count"]')


def test_follow_user_one_time(driver, live_server, login_user, user_factory, follow_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()
    follow_factory.create(follower=user2, following=user1)
    login_user(user2)
    driver.get(live_server.url + f'/users/{user1.pk}')
    follow_button = driver.find_element_by_css_selector('[data-test="follow"]')
    follow_button.click()
    follower_count = driver.find_element_by_css_selector('[data-test="follower-count"]').text
    assert '1' in follower_count
    following_count = driver.find_element_by_css_selector('[data-test="following-count"]').text
    assert '0' in following_count
