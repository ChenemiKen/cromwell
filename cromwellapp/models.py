from django.db import models

# Create your models here.
class Configs(models.Model):
    name = models.CharField(max_length=50, unique=True)
    switch = models.BooleanField()

    def __str__(self):
        return self.name