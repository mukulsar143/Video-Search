# videos/models.py

from django.db import models
from django.conf import settings

class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

class Subtitle(models.Model):
    video = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)
    text = models.TextField()
    start_time = models.FloatField()
    end_time = models.FloatField()
