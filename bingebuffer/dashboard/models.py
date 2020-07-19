from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Userprofile(models.Model):
    id=models.CharField(max_length=30,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    nickname = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    badge = models.CharField(max_length=30)

    def __str__(self):
        return self.id

class MovieReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    movie_id = models.CharField(max_length=30)
    movie_posterpath = models.CharField(max_length=30, default=None)
    movie_backdroppath = models.CharField(max_length=30, default=None)
    movie_name = models.CharField(max_length=30)
    movie_rating = models.IntegerField()
    movie_review = models.CharField(max_length=1000)
    review_title = models.CharField(max_length=100, default=None)
    review_slug = models.SlugField(default=None)
    review_public_status = models.BooleanField(default=False)
    review_hash = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + " " +  self.review_title