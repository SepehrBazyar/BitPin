import pytest
from django.contrib.auth.models import User

from ..models import Post, Rating


@pytest.mark.django_db
def test_ema_rating_initial():
    post = Post.objects.create(title="Foobar", content="Lorem Ipsum")
    user = User.objects.create_user(username="admin", password="qwerty")

    Rating.objects.create(post=post, user=user, score=4)

    post.refresh_from_db()
    assert post.ema_rating == 4.0


@pytest.mark.django_db
def test_ema_rating_multiple_updates():
    post = Post.objects.create(title="Foobar", content="Lorem Ipsum")
    user1 = User.objects.create_user(username="admin1", password="qwerty")
    user2 = User.objects.create_user(username="admin2", password="qwerty")
    user3 = User.objects.create_user(username="admin3", password="qwerty")

    Rating.objects.create(post=post, user=user1, score=5)
    post.refresh_from_db()
    assert post.ema_rating == 5.0

    Rating.objects.create(post=post, user=user2, score=3)

    alpha = 2 / (2 + 1)
    expected_ema_rating_2 = (3 * alpha) + (5.0 * (1 - alpha))

    post.refresh_from_db()
    assert post.ema_rating == pytest.approx(expected_ema_rating_2, 0.01)

    Rating.objects.create(post=post, user=user3, score=4)

    alpha = 2 / (3 + 1)
    expected_ema_rating_3 = (4 * alpha) + (expected_ema_rating_2 * (1 - alpha))

    post.refresh_from_db()
    assert post.ema_rating == pytest.approx(expected_ema_rating_3, 0.01)
