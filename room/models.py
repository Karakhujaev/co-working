from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=150, verbose_name="Name")
    type = models.CharField(max_length=11, choices=(("focus", "focus"), ("team", "team"), ("conference", "conference")), verbose_name="Type")
    capacity = models.IntegerField(verbose_name="Capacity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Added Time")
    modified_at = models.DateTimeField(auto_now=True,  verbose_name="Updated Time")