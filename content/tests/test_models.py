import pytest
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from ..models import Post, Rating


@pytest.mark.django_db
def test_create_post():
    post = Post.objects.create(title="Foobar", content="Lorem Ipsum")

    assert post.title == "Foobar"
    assert post.content == "Lorem Ipsum"
    assert post.is_deleted is False


@pytest.mark.django_db
def test_soft_delete_post():
    post = Post.objects.create(title="Foobar", content="Lorem Ipsum")
    post.delete()

    assert post.is_deleted is True
    assert Post.objects.filter(is_deleted=False).count() == 0


@pytest.mark.django_db
def test_create_rating():
    user = User.objects.create_user(username="admin", password="qwerty")
    post = Post.objects.create(title="Foobar", content="Lorem Ipsum")
    rating = Rating.objects.create(post=post, user=user, score=3)

    assert rating.score == 3


@pytest.mark.django_db
def test_unique_rating_per_user_post():
    user = User.objects.create_user(username="admin", password="qwerty")
    post = Post.objects.create(title="Foobar", content="Lorem Ipsum")
    Rating.objects.create(post=post, user=user, score=3)

    with pytest.raises(IntegrityError):
        Rating.objects.create(post=post, user=user, score=4)
