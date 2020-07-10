from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Userprofile(models.Model):
    id=models.CharField(max_length=30,primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    nickname = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    badge = models.CharField(max_length=30)

    def __str__(self):
        return self.id