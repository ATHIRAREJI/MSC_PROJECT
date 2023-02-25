from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    course = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True, verbose_name='Picture')
    profile_info = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

