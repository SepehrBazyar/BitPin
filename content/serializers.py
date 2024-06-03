from rest_framework import serializers

from .models import Post, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'id',
            'post',
            'user',
            'score',
        )


class PostSerializer(serializers.ModelSerializer):
    ratings_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'ratings_count',
            'average_rating',
        )
