from django.db import models

class User(models.Model):
    user_email = models.CharField(max_length=80, primary_key=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=80)
    image = models.FileField()

class Friendship(models.Model):
    first_user = models.CharField(max_length=80)
    second_user = models.CharField(max_length=80)

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_email = models.CharField(max_length=80)
    description = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    file = models.FileField()

    def __str__(self):
        return self.post_id

