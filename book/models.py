from django.db import models
from room.models import Room

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Resident(BaseModel):
    name = models.CharField(max_length=50)


class Booked(BaseModel):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

