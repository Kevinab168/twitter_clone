from pytest_factoryboy import register
from make_posts.tests.factories import UserFactory, PostFactory, FollowerFactory, FollowFactory
from make_posts.models import Post, Comment
import time


register(UserFactory)
register(PostFactory)
register(FollowerFactory)
register(FollowFactory)


def test_landing_page(driver, live_server):
    driver.get(live_server.url)
    assert "welcome" in driver.page_source.lower()
    assert driver.find_element_by_css_selector('[data-test="log_in"]')


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
    assert 'followers' in driver.page_source
    assert 'following' in driver.page_source
    assert 'posts' in driver.page_source
    assert driver.find_element_by_css_selector('[data-test="make-post"]')


def test_make_post(driver, login_user, live_server, user_factory):
    user = user_factory.create()
    login_user(user)
    driver.get(live_server.url + f'/users/{user.pk}')
    post_text = driver.find_element_by_css_selector('[data-test="post"]')
    post_text.send_keys('Sample Post')
    post_it = driver.find_element_by_css_selector('[data-test="make-post"]')
    post_it.click()
    assert 'Sample Post' in driver.page_source
    last_post = Post.objects.all().last()
    assert last_post.user == user


def test_make_comment(driver, live_server, login_user, user_factory, post_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(10):
        post_factory.create(user=user)
    driver.get(live_server + f'/users/{user.pk}')
    post_1 = driver.find_element_by_css_selector('[data-test="post-info"]')
    post_1.click()
    text_field = driver.find_element_by_css_selector('[data-test="text-input"]')
    text_field.send_keys('Sample1')
    submit_comment = driver.find_element_by_css_selector('[data-test="create-comment"]')
    submit_comment.click()
    assert 'Sample1' in driver.page_source
    recent_comment = Comment.objects.all().last()
    assert recent_comment.user == user
    assert recent_comment.post


def test_follow(driver, live_server, login_user, user_factory, post_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(10):
        post_factory.create(user=user)
    user2 = user_factory.create()
    login_user(user2)
    driver.get(live_server.url + f'/users/{user.pk}')
    follow_button = driver.find_element_by_css_selector('[data-test="follow"]')
    follow_button.click()
    follower_count = driver.find_element_by_css_selector('[data-test="follower-count"]').text
    assert '1' in follower_count
    following_count = driver.find_element_by_css_selector('[data-test="following-count"]').text
    assert '0' in following_count


def test_see_followers(driver, live_server, login_user, user_factory, follow_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(20):
        follow_factory.create(following=user)
    driver.get(live_server.url + f'/users/{user.pk}')
    followers_link = driver.find_element_by_css_selector('[data-test="follower-count"]')
    followers_link.click()
    followers_list = driver.find_elements_by_css_selector('[data-test="followers"]')
    assert len(followers_list) == 20
    assert 'Followers' in driver.page_source
