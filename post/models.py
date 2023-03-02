import uuid
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
def user_directory_path(instance, filename):
    # this defines the url for the uploading post, it would be like MEDIA_ROOT/user_{user_id}/filename
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_picture = models.ImageField(upload_to=user_directory_path, verbose_name='Post picture', null=False)
    post_caption = models.TextField(max_length=1500, verbose_name='Post caption')
    posted_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('postdetails', args=[str(self.id)])
    def __str__(self):
        return str(self.id)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Following')

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted_date, following=user)
            stream.save()

class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_liked')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_liked')
#Once post saved, add_post function within the stream class will be called , here the sender is Post class
post_save.connect(Stream.add_post, sender=Post)
