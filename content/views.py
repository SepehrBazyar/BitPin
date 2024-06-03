from uuid import UUID

from django.db.models import Avg, Count
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Rating
from .serializers import (
    PostSerializer,
    RatingSerializer,
)

# Create your views here.
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.annotate(
            ratings_count=Count('ratings'),
            average_rating=Avg('ratings__score')
        )

    def list(self, request: Request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        for post_data in serializer.data:
            post_id = post_data['id']
            user_rating = Rating.objects.filter(
                post_id=post_id,
                user=request.user,
            ).first()
            post_data['user_rating'] = user_rating.score if user_rating else None

        return Response(serializer.data)


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
