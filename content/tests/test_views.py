import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Post, Rating


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    return User.objects.create_user(username="admin", password="qwerty")


@pytest.mark.django_db
def test_post_list_view(api_client, create_user):
    Post.objects.create(title="Foo", content="Lorem Ipsum")
    Post.objects.create(title="Bar", content="Lorem Ipsum")

    api_client.force_authenticate(user=create_user)

    response = api_client.get(reverse("content:post-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_rate_post(api_client, create_user):
    post = Post.objects.create(title="Foobar", content="Lorem Ipsum")

    api_client.force_authenticate(user=create_user)

    url = reverse("content:post-rate", args=[post.id])
    response = api_client.post(
        url,
        data={
            "score": 4,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["is_created"] is True

    # Update the rating
    response = api_client.post(
        url,
        data={
            "score": 5,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["is_created"] is False

    # Check the updated rating
    rating = Rating.objects.get(post=post, user=create_user)
    assert rating.score == 5
