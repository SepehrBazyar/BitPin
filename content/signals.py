from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Rating


@receiver(post_save, sender=Rating)
def update_post_ema(sender, instance: Rating, **kwargs):
    post = instance.post
    rating_count = post.ratings.count()
    if rating_count == 1:
        post.ema_rating = instance.score
    else:
        alpha = 2 / (rating_count + 1)
        post.ema_rating = (instance.score * alpha) + (post.ema_rating * (1 - alpha))

    post.save()
