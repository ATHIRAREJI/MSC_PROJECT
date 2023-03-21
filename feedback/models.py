from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    sentimental_status = models.IntegerField(help_text="1-Positive, 0-Negative")
    date = models.DateTimeField(auto_now_add=True)

    

