from django.db import models
from django.contrib.auth.models import User
from post.models import Post

# Create your models here.
class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="post")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    


