from django.db import models


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user_email = models.CharField(max_length=80)
    description = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    file = models.FileField()

    def __str__(self):
        return self.post_id

