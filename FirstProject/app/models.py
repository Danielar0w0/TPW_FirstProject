from django.db import models


class User(models.Model):
    user_email = models.CharField(max_length=80, primary_key=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=80)
    image = models.FileField()

    def update_image(self, file):
        self.image.storage.delete(self.image.name)
        self.image = file


class Friendship(models.Model):
    first_user = models.CharField(max_length=80)
    second_user = models.CharField(max_length=80)


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    file = models.FileField()

    def delete(self):
        self.file.storage.delete(self.file.name)
        super().delete()

    def __str__(self):
        return self.post_id


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)

    def __str__(self):
        return self.comment_id
