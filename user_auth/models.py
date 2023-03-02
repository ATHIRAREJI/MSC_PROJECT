from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    course = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True, verbose_name='Picture')
    profile_info = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance,**kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender = User)
post_save.connect(save_user_profile, sender = User)