from rest_framework import serializers

from .models import Post


class RatingSerializer(serializers.Serializer):
    score = serializers.IntegerField(min_value=0, max_value=5)


class RatingResponseSerializer(serializers.Serializer):
    is_created = serializers.BooleanField()


class PostSerializer(serializers.ModelSerializer):
    ratings_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    user_rating = serializers.IntegerField(
        required=False,
        default=None,
        min_value=0,
        max_value=5,
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'ratings_count',
            'average_rating',
            'user_rating',
        )
