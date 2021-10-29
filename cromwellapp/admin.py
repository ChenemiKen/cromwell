from django.contrib import admin
from cromwellapp import models

# Register your models here.
admin.site.register(models.Config)
admin.site.register(models.Project)