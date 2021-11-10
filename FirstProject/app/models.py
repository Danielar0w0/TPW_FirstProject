from django.db import models


class Post(models.Model):
    post_id = models.IntegerField()
    username = models.CharField(max_length=70)
    description = models.CharField(max_length=256)
    date = models.DateField() # or DateTimeField()?
    file_path = models.FilePathField()

    def __str__(self):
        return self.post_id
