from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

sentiment = (
        ('1','Happy'),
        ('2','Meh'),
        ('3','Sad')
    )



class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Entry(models.Model):
    host = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True)
    record = models.TextField( null = False)
    created_at = models.DateField(auto_now_add=True, auto_now=False)
    highlight = models.CharField(max_length = 200)
    sentiment = (
        ('H','Happy'),
        ('M','Meh'),
        ('S','Sad')
    )
    mood = models.CharField(choices = sentiment, max_length=10, null=True)
    def __str__(self):
        return str(self.created_at)



    
