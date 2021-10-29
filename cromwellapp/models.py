from django.db import models

# Create your models here.
class Config(models.Model):
    name = models.CharField(max_length=50, unique=True)
    switch = models.BooleanField()

    def __str__(self):
        return self.name

class Project(models.Model):
    proj_id = models.IntegerField()
    title = models.CharField(max_length=200, blank=True, null=True)
    cate_id = models.IntegerField( blank=True, null=True)
    cate_name = models.CharField(max_length=50, blank=True, null=True)
    proj_description = models.CharField(max_length=2000, blank=True, null=True)
    posted_date = models.DateTimeField(blank=True, null= True)

    def __str__(self):
        return ("%d -- %s" %(self.proj_id,self.title))
