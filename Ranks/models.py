# Ranks.models.py
from django.db import models
from django.apps import apps

class Rank(models.Model):
    
    title = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='ranks_icons', default='default_tag_image.png')
    
    def __str__(self):
        return str(self.title)
