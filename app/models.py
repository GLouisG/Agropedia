from django.db import models

# Create your models here.
class Plants(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField()
  temperature = models.IntegerField()
  elevation = models.IntegerField()
