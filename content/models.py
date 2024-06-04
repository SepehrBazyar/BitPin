from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .managers import CustomManager


# Create your models here.
class AbstractBaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)

    class Meta:
        abstract = True


class BaseModel(AbstractBaseModel):
    objects = CustomManager()

    is_deleted = models.BooleanField(default=False, db_index=True)

    def delete(self):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class Post(BaseModel, TimeStampMixin):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.title


class Rating(BaseModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
    )

    class Meta:
        unique_together = (("post", "user"),)
