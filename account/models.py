from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to='photo_up')
    sex = models.CharField(max_length=20)
    motto = models.CharField(max_length=200)

    def __str__(self):
        return self.username

class Passage(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    article = models.TextField()
    time = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to='upload')

    def __str__(self):
        return self.author