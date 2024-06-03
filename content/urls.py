from django.urls import path

from .views import PostListView, RatingCreateUpdateView


app_name, urlpatterns = 'content', [
    path('posts/', PostListView.as_view(), name='post-list'),
    path(
        'posts/<uuid:post_id>/rate/',
        RatingCreateUpdateView.as_view(),
        name='post-rate',
    ),
]
