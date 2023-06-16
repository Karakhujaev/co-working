from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=11, choices=(("focus", "focus"), ("team", "team"), ("conference", "conference")))
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)