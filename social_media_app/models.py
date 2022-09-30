from django.db import models
# Create your models here.


class Users(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    password = models.TextField(blank=True)

    class Meta:
        db_table = u'"users_data"'

    def __str__(self):
        return self.email


class Followers(models.Model):
    follower = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='follower', related_name='follower')
    following_to = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='following_to', related_name='following_to')

    class Meta:
        db_table = u'"followers"'


class Posts(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = u'"posts"'


class Comments(models.Model):
    comment = models.TextField()
    post_id = models.ForeignKey(Posts,  on_delete=models.CASCADE, db_column='post_id')
    commented_by = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='commented_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = u'"comments"'


class Likes(models.Model):
    post_id = models.ForeignKey(Posts,  on_delete=models.CASCADE, db_column='post_id')
    liked_by = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='liked_by')
    liked_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = u'"likes"'
