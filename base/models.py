from django.db import models


# Create your models here.
class Post(models.Model):
    url = models.CharField(max_length=150, blank=True, null=True)

