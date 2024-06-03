from uuid import UUID

from django.db.models import Avg, Count
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Rating
from .paginations import CustomPagination
from .serializers import (
    PostSerializer,
    RatingSerializer,
)

# Create your views here.
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self):
        return Post.objects.annotate(
            ratings_count=Count('ratings'),
            average_rating=Avg('ratings__score')
        )

    def list(self, request: Request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)

            for post_data in paginated_response.data['results']:
                post_id = post_data['id']
                user_rating = Rating.objects.filter(
                    user=user,
                    post_id=post_id,
                ).first()
                post_data['user_rating'] = user_rating.score if user_rating else None

            return paginated_response


class RatingCreateUpdateView(APIView):
    def post(self, request: Request, post_id: UUID):
        post = generics.get_object_or_404(Post, id=post_id)
        score = request.data.get('score')

        # if score is None or not (0 <= int(score) <= 5):
        #     return Response(
        #         {"error": "Invalid score"},
        #         status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        #     )

        rating, _ = Rating.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={
                'score': score,
            },
        )

        return Response(
            RatingSerializer(instance=rating).data,
            status=status.HTTP_201_CREATED,
        )
